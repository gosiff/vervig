import copy
from PyQt4 import QtCore
import os
from Commands import Invoker, AddFeatureCommand, DeleteFeatureCommand
from model.fuse import Fuse
from model.roomTableModel import RoomTableModel
from model.TreeItemModel import TreeModel, CustomNode
from model.room import Room
import time

from model.socket import Socket

__author__ = 'Fredrik Salovius'


class HouseModel(QtCore.QObject):
    updated = QtCore.pyqtSignal()
    # featureCreated = QtCore.pyqtSignal()

    def __init__(self):
        super(HouseModel, self).__init__()
        self.fuse_list = []
        self.rooms = []
        self.__num_sockets = 0
        self._features = dict()
        self._room_table_model = RoomTableModel(self)
        self._fuse_tree_item_model = TreeModel(self)
        self._background_image = ''
        self.fuse_not_set_node = CustomNode('undefined')
        self._fuse_tree_item_model.addNewChild(self.fuse_not_set_node)
        self._background_image_data = QtCore.QByteArray()
        self._invoker = Invoker()
        self._rotation = 0.0
        self._fuse_list = []
        print 'init house model'

    def __getstate__(self):
        """
        Return the __dict__ of the object, stripped from contents that doesn't need serialization.
        :return: dict
        """

        d = copy.copy(self.__dict__)
        del d['_room_table_model']  # Do not save easily re-creatable table models
        del d['_fuse_tree_item_model']
        del d['_invoker']

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

        del state['_background_image']

        if '_background_image_data' not in state:
            print "Detected old version of saved file!"
            self._background_image_data = QtCore.QByteArray()

        if isinstance(state['_features'], list):
            for feature in state['_features']:
                self._append_feature(feature)

            del state['_features']


        self.__init__()
        self.__dict__.update(state)

    def add_room(self, pos=None):

        if pos is not None:
            new_room = self.add_room()
            new_room._set_pos(pos)
        else:
            new_room = Room('New Room')
            # self._camera_table_model.begin_append()
            self.add_feature(new_room)
            # self._camera_table_model.end_append()

        return new_room

    def delete_room(self, id_or_room):
        if isinstance(id_or_room, Room):
            self.delete_feature(id_or_room)
        else:
            room = self.get_feature_by_id(id_or_room)
            self.delete_feature(room)
        self.updated.emit()

    def add_socket(self, pos=None):
        """
        :param pos: QPointF (QPointF.x(), QPointF.y())
        Callback method for what happens when the user clicks the Add Camera button in the GUI
        """
        if pos is not None:
            new_socket = self.add_socket()
            new_socket._set_pos(pos)
        else:
            new_socket = Socket('New Socket')
            self._fuse_tree_item_model.addNewChild(new_socket)
            self.add_feature(new_socket)
            # self._camera_table_model.end_append()

        return new_socket

    def delete_socket(self, id_or_socket):
        if isinstance(id_or_socket, Socket):
            self.delete_feature(id_or_socket)
        else:
            socket = self.get_feature_by_id(id_or_socket)
            self.delete_feature(socket)
        self.updated.emit()

    def add_fuse(self, pos=None):
        new_fuse = Fuse('New Fuse')
        self.add_feature(new_fuse)


    def remove_fuse(self, id_or_fuse):
        if isinstance(id_or_fuse, Fuse):
            self.delete_feature(id_or_fuse)
        else:
            fuse = self.get_feature_by_id(id_or_fuse)
            self.delete_feature(fuse)
        self.updated.emit()

    def update(self):
        print 'something has updated'

    def get_all_rooms(self):
        return [x for x in self._features.values() if x.get_feature_type() == 'Room']

    def get_all_sockets(self):
        return [x for x in self._features.values() if x.get_feature_type() == 'Socket']

    def get_all_fuses(self):
        return self._fuse_list

    def get_room_name_by_id(self, _id):
        lst = self.get_all_sockets()
        for room in lst:
            if _id == room.get_id():
                return room.get_name()
        return None

    def get_feature_by_id(self, id_):
        return self._features[id_]

    def get_invoker(self):
        return self._invoker

    def _append_feature(self, feature):
        new_key = 0
        if len(self._features) > 0:
            new_key = max(k for k, v in self._features.iteritems()) + 1
        self._features[new_key] = feature

    def _remove_feature(self, feature):
        res = list(k for k, v in self._features.iteritems() if v is feature)
        for key in res:
            self._features.pop(key)
        self.updated.emit()

    def add_feature_without_update(self, feature):
        self._append_feature(feature)
        feature.set_model(self)  # update the feature with a reference to the range object (self)

    def get_features(self):
        return self._features

    def _set_features(self, features):
        self._features = features
        self.get_camera_table_model().updateAll()
        # self.get_target_table_model().updateAll() # updated.emit() calls this anyway
        self.updated.emit()

    def _add_feature(self, feature):
        self.add_feature_without_update(feature)
        self.updated.emit()

    def add_feature(self, feature):
        cmd = AddFeatureCommand(self._add_feature, self._set_features, self._features, feature)
        self.get_invoker().store_and_execute(cmd)

    def _delete_feature_without_update(self, feature):
        self._remove_feature(feature)

    def _delete_feature(self, feature):
        self._delete_feature_without_update(feature)
        self.updated.emit()

    def delete_feature(self, feature):
        """
        Deletes the specified feature (Camera, CalibrationPoint, Target,...)
        :param feature:
        :return:
        """
        cmd = DeleteFeatureCommand(self._delete_feature, self._set_features, self._features, feature)
        self.get_invoker().store_and_execute(cmd)

    def get_room_table_model(self):
        return self._room_table_model

    def get_fuse_tree_item_model(self):
        return self._fuse_tree_item_model

    def update_save_time(self):
        return time.time()

    def set_background_image(self, image_file):
        relative_path = os.path.relpath(os.path.normpath(image_file),
                                          os.path.normpath(self.project_path))
        self._background_image = relative_path

    def get_background_image(self):
        return os.path.join(self.project_path, self._background_image)

    def set_background_image_data(self, data):
        self._background_image_data = data

    def get_background_image_data(self):
        return self._background_image_data

    def get_rotation(self):
        return self._rotation