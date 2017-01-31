from model.features import ElectricFeature
from PyQt4 import QtCore
import copy

__author__ = 'Fredrik Salovius'


class LampOutlet(ElectricFeature):

    deleteRequested = QtCore.pyqtSignal()

    def __init__(self, name, fuse):
        super(LampOutlet, self).__init__(name, 'Lamp', fuse)
        self._column_count = 1


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

        self.__init__(state['_name'], state['_fuse'])
        self.__dict__.update(state)

    def prepare_for_deletion(self):
        self.get_model().delete_lamp(self)

    def columnCount(self):
        return self._column_count

    def childCount(self):
        return len(self.get_all_children())

    def child(self, row):
        if row >= 0 and row < self.childCount():
            return self.get_all_children()[row]

    def parent(self):
        return self.get_fuse()

    def row(self):
        return self._row

    def get_all_children(self):
        return [x for x in self.get_model().get_all_switch() if x.get_lamp() == self]

    def addChild(self, child):
        old_parent = child.get_lamp()
        child.set_lamp(self)
        child._row = len(self.get_all_children())
        self.updated.emit()
        if old_parent != None:
            old_parent.updated.emit()
        self.get_model().lampChanged.emit()
