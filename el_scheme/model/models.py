__author__ = 'Fredrik Salovius'
from PyQt4 import QtCore

class Socket(QtCore.QObject):
    def __init__(self, _id):
        super(Socket,self).__init__()
        self.__id = _id
        self.__location = None
        self.__fuse_id = None

    def get_id(self):
        return self.__id


    def get_location(self):
        return self.__location

    def set_location(self, loc):
        self.__location = loc

    def set_fuse_id(self, _id):
        self.__fuse_id = _id

    def get_fuse_id(self):
        return self.__fuse_id

