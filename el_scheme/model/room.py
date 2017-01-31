from Commands import GenericSetCommand, BatchCommand
from model.features import HouseFeature

__author__ = 'Fredrik Salovius'
import copy
from PyQt4 import QtCore
from PyQt4.QtCore import QPointF


class Room(HouseFeature):

    deleteRequested = QtCore.pyqtSignal()

    def __init__(self, name, description=None):
        super(Room, self).__init__(name, description)
        self.socket_list = {}
        self.__x = 0        # pixels
        self.__y = 0        # pixles
        self.width = 2      # meter
        self.height = 2     # meter
        self._floor = 0
        self._rotation = 0.0
        self._locked = False
        self._selected = False
        self.bounding_box = [QPointF(0,0), QPointF(100,0),QPointF(100,100),QPointF(0,100)]

    def __getstate__(self):
        d = copy.copy(self.__dict__)
        del d['_graphics_item']
        del d['_graphics_widget']
        return d

    def __setstate__(self, state):
        """
        Define deserialization of object from the state-dict.
        :param state:
        :return:
        """

        """# Support adding a new member not previously defined in the class
        if 'new_member' not in state:
            self.new_member = "new value"
        self.__dict__.update(state)"""

        """ # Support removing old members not in new version of class
        if 'old_member' in state:
            # If you want: do something with the old member
            del state['old_member']
        self.__dict__.update(state) """

        self.__init__("")
        self.__dict__.update(state)

    def set_socket(self, socket_id, fuse_id):
        self.socket_list[socket_id] = fuse_id

    def set_floor(self, floor_level):
        self._floor = floor_level

    def get_feature_type(self):
        return 'Room'

    def get_floor(self):
        return self._floor

    def get_sockets(self):
        return len(self.socket_list)

    def get_pos(self):
        """
        Returns the image position of the feature i screen coordinates (pixels)
        :return: QtCore.QPointF(x,y)
        """
        return QtCore.QPointF(self.__x, self.__y)

    def _set_pos(self, new_pos):
        """
        new_pos is given in screen coordinates (pixels). Updates position without issuing a command.
        :param new_pos: QtCore.QPointF(x, y)
        :return:
        """
        self.__x = new_pos.x()
        self.__y = new_pos.y()
        self.updated.emit()

    def set_pos(self, new_pos):
        """
        new_pos is given in screen coordinates (pixels)
        :param new_pos: QtCore.QPointF(x, y)
        :return:
        """
        if self._locked:
            return

        cmd = GenericSetCommand(self._set_pos, self.get_pos, new_pos)
        self.get_model().get_invoker().store_and_execute(cmd)

    def get_rotation(self):
        return self._rotation

    def set_locked(self, bool_):
        """
        Set whether the camera should be movable or not. True indicates that the CameraItem should NOT be movable.
        :param bool_:
        :return:
        """
        self._locked = bool_

    def is_locked(self):
        """
        Returns whether the camera should be movable by the user or not.
        IDEA: lock camera on a model-level instead, i.e. don't allow changes of the underlying model, instead of letting
        the front end check if it's "allowed" to change it. This method will still be used by the front end to
        display for the user whether a camera is locked or not.
        :return: True or False
        """
        return self._locked

    def get_rotation(self):
        """
        Returns the yaw-rotation (pan-rotation) of the camera, in degrees.
        :return: rotation: float
        """
        return self._rotation

    def _set_rotation(self, new_rotation):
        """
        Sets the yaw-rotation to the provided float, in degrees, without issuing a command.
        :param new_rotation: float
        :return:
        """
        if self._locked:
            return

        self._rotation = new_rotation
        self.updated.emit()

    def set_rotation(self, new_rotation):
        """
        Sets the yaw-rotation to the provided float, in degrees.
        :param new_rotation: float
        :return:
        """
        if self._locked:
            return
        cmd = GenericSetCommand(self._set_rotation, self.get_rotation, new_rotation)
        self.get_house().get_invoker().store_and_execute(cmd)

    def prepare_for_deletion(self):
        self.get_model().delete_room(self)

    def is_selected(self):
        return self._selected

    def set_selected(self):
        self._selected = not self._selected

    def _set_floor(self, value):
        self._floor = value

    def get_floor(self):
        return self._floor

    def set_properties_from_widget(self, name, floor, socket_listx, description):
        """
        Applies properties entered by user in the CameraInfoWidget. If the intrinsics_filename has been set, load
        new intrinsic parameters from file.
        :param name: str
        :param mac: str
        :param rotation: float (degrees)
        :param pos: QtCore.QPointF (x and z coordinate of the camera's real-world position). TODO: Confusing, I know...
        :param intrinsics_filename: str
        :return:
        """
        if self._locked:
            return

        cmd1 = GenericSetCommand(self._set_name, self.get_name, name)
        cmd2 = GenericSetCommand(self._set_floor, self.get_floor, floor)
        cmd3 = GenericSetCommand(self._set_description,  self.get_description, description)

        commands = [cmd1, cmd2, cmd3]
        self.get_model().get_invoker().store_and_execute(BatchCommand(commands))
        self.updated.emit()
