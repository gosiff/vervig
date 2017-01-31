import os

from PyQt4 import QtGui
from PyQt4 import uic

from calibrator.StringUtils import resource_path

__author__ = 'Fredrik Salovius'

class ListView(QtGui.QWidget):

    def __init__(self, model, parent=None):
        super(ListView, self).__init__(parent)
        uic.loadUi(resource_path(os.path.join("ui", "mainview_table.ui")), self)

        self.fuseTable = self.findChild(QtGui.QTableView, "fuseTableView")
        self.socketTable = self.findChild(QtGui.QTableView, "socketTableView")
        self.roomTable = self.findChild(QtGui.QTableView, "roomTableView")

        self.fuseTable.setModel(model.get_fuse_table_model())
        self.socketTable.setModel(model.get_socket_table_model())
        self.roomTable.setModel(model.get_room_table_model())

        self.fuseTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.socketTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.roomTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.fuseTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.socketTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.roomTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        # self.fuseTable.setItemDelegateForColumn(range_.get_camera_table_model().columnCount() - 1,
        #                                         DeleteTableRowDelegate(self.cameraTable, range_.request_delete_camera))
        #
        # self.socketTable.setItemDelegateForColumn(range_.get_camera_table_model().columnCount() - 1,
        #                                           DeleteTableRowDelegate(self.cameraTable, range_.request_delete_cam
        #
        # self.roomTable.setItemDelegateForColumn(range_.get_target_table_model().columnCount() - 1,
        #                                           DeleteTableRowDelegate(self.targetTable, range_.delete_target))

