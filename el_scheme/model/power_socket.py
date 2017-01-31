from model.features import ElectricFeature
import copy
from PyQt4 import QtCore

__author__ = 'Fredrik Salovius'


class Socket(ElectricFeature):

    deleteRequested = QtCore.pyqtSignal()

    def __init__(self, name, fuse):
        super(Socket, self).__init__(name, 'Socket', fuse)
        self.socket_list = {}
        self._room_id = None
        self._outlets = 2
        self.set_fuse(fuse)

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

        self.__init__("", state['_fuse'])
        self.__dict__.update(state)


    def prepare_for_deletion(self):
        self.get_model().delete_socket(self)

    def get_outlets(self):
        return self._outlets

    def set_outlets(self, value):
        self._outlets = value
