from PyQt4 import QtCore

from Commands import GenericSetCommand
from model.features import ElectricFeature
import copy
__author__ = 'Fredrik Salovius'


class Switch(ElectricFeature):

    deleteRequested = QtCore.pyqtSignal()

    def __init__(self, name, fuse, lamp):
        super(Switch, self).__init__(name, 'Switch', fuse)
        self.__lamp = lamp

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
        self.__init__(state['_name'], state['_fuse'], state['_Switch__lamp'])

        self.__dict__.update(state)

    def prepare_for_deletion(self):
        self.get_model().delete_switch(self)

#    def get_lamp_outlets(self):
#    return [lamp_outlet for lamp_outlet in self.get_model().get_all_lamp_outlets() if self in lamp_outlet.get_switch]

    def get_lamp(self):
        """
        Returns the image position of the feature i screen coordinates (pixels)
        :return: QtCore.QPointF(x,y)
        """
        return self.__lamp

    def _set_lamp(self, new_lamp):
        """
        new_pos is given in screen coordinates (pixels). Updates position without issuing a command.
        :param new_pos: QtCore.QPointF(x, y)
        :return:
        """
        self.__lamp = new_lamp
        self.updated.emit()

    def set_lamp(self, new_lamp):
        """
        new_pos is given in screen coordinates (pixels)
        :param new_pos: QtCore.QPointF(x, y)
        :return:
        """
        cmd = GenericSetCommand(self._set_lamp, self.get_lamp, new_lamp)
        self.get_model().get_invoker().store_and_execute(cmd)

    def parent(self):
        return self.get_lamp()

    def get_fuse(self):
        return self.__lamp.get_fuse()