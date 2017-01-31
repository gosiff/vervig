import copy
from PyQt4 import QtCore
import os
from Commands import Invoker, AddFeatureCommand, DeleteFeatureCommand
from model.fuse import Fuse
from model.fuseTableModel import FuseTableModel
from model.lamp import LampOutlet
from model.socketTableModel import SocketTableModel
from model.roomTableModel import RoomTableModel
from model.TreeItemModel import TreeModel, CustomNode
from model.room import Room
import time

from model.power_socket import Socket
from model.switch import Switch

__author__ = 'Fredrik Salovius'


class HouseModel(QtCore.QObject):
    updated = QtCore.pyqtSignal()
    fuseChanged = QtCore.pyqtSignal()
    lampChanged = QtCore.pyqtSignal()
    # featureCreated = QtCore.pyqtSignal()

    def __init__(self):
        super(HouseModel, self).__init__()
        self._features = dict()
        self._room_table_model = RoomTableModel(self)
        self._socket_table_model = SocketTableModel(self)
        self._fuse_table_model = FuseTableModel(self)
        self._fuse_tree_item_model = TreeModel(self)
        self._background_image = ''
        self._background_image_data = QtCore.QByteArray()
        self._invoker = Invoker()
        self._rotation = 0.0
        print 'init house model'
        self.updated.connect(self._fuse_table_model.updateAll)

    def __getstate__(self):
        """
        Return the __dict__ of the object, stripped from contents that doesn't need serialization.
        :return: dict
        """

        d = copy.copy(self.__dict__)
        del d['_room_table_model']  # Do not save easily re-creatable table models
        del d['_socket_table_model']  # Do not save easily re-creatable table models
        del d['_fuse_table_model']  # Do not save easily re-creatable table models
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

        if isinstance(state['_features'], dict):

            for _id, feature in state['_features'].iteritems():
                if feature.get_feature_type() == 'Fuse':
                    self._fuse_tree_item_model.addChild(feature, None)

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
        if len(self.get_all_fuses()) == 0:
            print 'No fuse'
            return
        if pos is not None:
            obj = self.add_socket()
            obj._set_pos(pos)
        else:
            fuse = self.get_all_fuses()[0]
            name = 'Socket-' + str(len(self.get_all_sockets()) + 1)
            obj = Socket(name, fuse)
            self.add_feature(obj)
            fuse.addChild(obj)
            # self._camera_table_model.end_append()

        return obj

    def delete_socket(self, id_or_obj):
        if isinstance(id_or_obj, Socket):
            self.delete_feature(id_or_obj)
        else:
            obj = self.get_feature_by_id(id_or_obj)
            self.delete_feature(obj)
        self.updated.emit()

    def add_lamp(self, pos=None):
        """
        :param pos: QPointF (QPointF.x(), QPointF.y())
        Callback method for what happens when the user clicks the Add Camera button in the GUI
        """
        if len(self.get_all_fuses()) == 0:
            print 'No fuse'
            return
        if pos is not None:
            obj = self.add_lamp()
            obj._set_pos(pos)
        else:
            fuse = self.get_all_fuses()[0]
            name = 'Lamp-Outlet-' + str(len(self.get_all_lamp_outlets()) + 1)
            obj = LampOutlet(name, fuse)
            self.add_feature(obj)
            fuse.addChild(obj)

            # self._camera_table_model.end_append()

        return obj

    def delete_lamp(self, id_or_obj):
        if isinstance(id_or_obj, LampOutlet):
            self.delete_feature(id_or_obj)
        else:
            obj = self.get_feature_by_id(id_or_obj)
            self.delete_feature(obj)
        self.updated.emit()

    def add_switch(self, pos=None):
        """
        :param pos: QPointF (QPointF.x(), QPointF.y())
        Callback method for what happens when the user clicks the Add Camera button in the GUI
        """
        if len(self.get_all_fuses()) == 0:
            print 'No fuse'
            return

        if len(self.get_all_lamp_outlets()) == 0:
            print 'No lamp outlets'
            return

        if pos is not None:
            obj = self.add_switch()
            obj._set_pos(pos)
        else:
            lamp = self.get_all_lamp_outlets()[0]
            name = 'Switch-' + str(len(self.get_all_switch()) + 1)
            obj = Switch(name, self.get_all_fuses()[0], lamp)
            self.add_feature(obj)
            lamp.addChild(obj)

            # self._camera_table_model.end_append()

        return obj

    def delete_switch(self, id_or_obj):
        if isinstance(id_or_obj, Switch):
            self.delete_feature(id_or_obj)
        else:
            obj = self.get_feature_by_id(id_or_obj)
            self.delete_feature(obj)
        self.updated.emit()

    def add_fuse(self, pos=None):
        if pos is not None:
            new_fuse = self.add_fuse()
            new_fuse._set_pos(pos)
        else:
            _id = len(self.get_all_fuses()) + 1
            name = 'Fuse-' + str(_id)
            new_fuse = Fuse( name, _id)
            self.add_feature(new_fuse)
            self._fuse_tree_item_model.addChild(new_fuse, None)
        return new_fuse

    def delete_fuse(self, id_or_fuse):
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
        return [x for x in self._features.values() if x.get_feature_type() == 'Fuse']

    def get_all_lamp_outlets(self):
        return [x for x in self._features.values() if x.get_feature_type() == 'Lamp']

    def get_all_switch(self):
        return [x for x in self._features.values() if x.get_feature_type() == 'Switch']

    def get_all_children_of_fuse(self, fuse):
        lst = list()
        for x in self._features.values():
            if x.get_feature_type() != 'Fuse' and x.get_feature_type() != 'Room' and x.get_feature_type() != 'Switch':
                if x.get_fuse() == fuse:
                    lst.append(x)
        return lst

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

    def get_socket_table_model(self):
        return self._socket_table_model

    def get_fuse_table_model(self):
        return self._fuse_table_model

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