from model.features import HouseFeature
import copy
from PyQt4 import QtCore
from Commands import GenericSetCommand

__author__ = 'Fredrik Salovius'


class Socket(HouseFeature):

    deleteRequested = QtCore.pyqtSignal()

    def __init__(self, name):
        super(Socket, self).__init__(name)
        self.socket_list = {}
        self.__x = 0  # pixels
        self.__y = 0  # pixles
        self._locked = False
        self._selected = False
        self._room_id = None
        self._fuse_id = None
        self._outlets = 2

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

    def get_position_in_room_x(self):
        return self._x

    def get_position_in_room_y(self):
        return self._y

    def set_position_in_room_x(self, value):
        self._x = value

    def set_position_in_room_y(self, value):
        self._y = value

    def get_feature_type(self):
        return 'Socket'

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

    def prepare_for_deletion(self):
        self.get_model().delete_socket(self)

    def is_selected(self):
        return self._selected

    def set_selected(self):
        self._selected = not self._selected

    def get_room_id(self):
        return self._room_id

    def set_room_id(self, _id):
        self._room_id = _id

    def get_fuse_id(self):
        return self._fuse_id

    def set_fuse_id(self, _id):
        self._fuse_id = _id

    def get_outlets(self):
        return self._outlets

    def set_outlets(self, value):
        self._outlets = value