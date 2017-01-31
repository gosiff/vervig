from PyQt4 import QtCore

from Commands import GenericSetCommand
from model.features import HouseFeature
import copy

from model.power_socket import Socket

__author__ = 'Fredrik Salovius'


class Fuse(HouseFeature):

    deleteRequested = QtCore.pyqtSignal()

    def __init__(self, name, _id):
        super(Fuse, self).__init__(name)
        self._fuse_id = _id
        self._column_count = 2
        self.__x = 1
        self.__y = 1
        self.__nominal_current = 10
        self.__cable_dimension = 1


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

        self.__init__("", state['_fuse_id'])
        self.__dict__.update(state)

    def columnCount(self):
        return self._column_count

    def childCount(self):
        return len(self.get_all_children())

    def child(self, row):
        if row >= 0 and row < self.childCount():
            return self.get_all_children()[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def get_all_children(self):
        return self.get_model().get_all_children_of_fuse(self)

    def addChild(self, child):
        old_parent = child.get_fuse()
        child.set_fuse(self)
        child._row = len(self.get_all_children())
        self.updated.emit()
        if old_parent is not None:
            old_parent.updated.emit()
        self.get_model().fuseChanged.emit()

    def get_feature_type(self):
        return 'Fuse'

    def get_fuse_id(self):
        return self._fuse_id

    def set_fuse_id(self, value):
        self._fuse_id = value
        self.updated.emit()

    def data(self, column):
        return self.get_name()

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
        cmd = GenericSetCommand(self._set_pos, self.get_pos, new_pos)
        self.get_model().get_invoker().store_and_execute(cmd)

    def set_properties_from_widget(self, _id, _nc, _cd):
        self.set_name('Fuse-' + str(_id))
        self.set_fuse_id(_id)
        self.set_nominal_current(_nc)
        self.set_cable_dimension(_cd)

    def prepare_for_deletion(self):
        self.get_model().delete_fuse(self)

    def _set_nominal_current(self, value):
        self.__nominal_current = value
        self.updated.emit()

    def set_nominal_current(self, value):
        cmd = GenericSetCommand(self._set_nominal_current, self.get_nominal_current, value)
        self.get_model().get_invoker().store_and_execute(cmd)

    def get_nominal_current(self):
        return self.__nominal_current

    def _set_cable_dimension(self, value):
        self.__cable_dimension = value
        self.updated.emit()

    def set_cable_dimension(self, value):
        cmd = GenericSetCommand(self._set_cable_dimension, self.get_cable_dimension, value)
        self.get_model().get_invoker().store_and_execute(cmd)

    def get_cable_dimension(self):
        return self.__cable_dimension

