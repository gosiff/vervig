from view.image_view import HouseImageView
from view.main_view_table import ListView

__author__ = 'Fredrik Salovius'
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4 import QtCore
from StringUtils import resource_path
from view.add_room_dialog import AddRoomDialog
import os

style = '''
QListView {
    show-decoration-selected: 1;
    selection-color: white;
    selection-background-color: #0068d9;
}

QListView::item:selected:active:hover{
    background-color: #0068d9; color: white;
}
QListView::item:selected:active:!hover{
    background-color: #0068d9; color: white;
}
QListView::item:selected:!active{
    background-color: #0068d9; color: white;
}
QListView::item:!selected:hover{
    background-color:green; color: white;
}
QGraphicsView{
    border-style: none;
}
'''

class MainviewWidget(QtGui.QWidget):

    readyForAddRoom = QtCore.pyqtSignal()


    def __init__(self, model, parent=None):
        super(MainviewWidget, self).__init__(parent)

        self.model = model

        self.list_view = ListView(self.model)

        uic.loadUi(resource_path(os.path.join("ui", "mainview_widget.ui")), self)
        tabWidget = self.findChild(QtGui.QTabWidget, "tabWidget")
        self.image_view = HouseImageView(self.model)
        tabWidget.addTab(self.image_view, "Overview")
        tabWidget.addTab(self.list_view, "List View")

        self.loadImagePushbutton = self.findChild(QtGui.QPushButton, "loadImagePushButton")
        self.addRoomPushbutton = self.findChild(QtGui.QPushButton, "addRoomPushButton")
        self.addSocketPushbutton = self.findChild(QtGui.QPushButton, "addSocketPushButton")
        self.addFusePushbutton = self.findChild(QtGui.QPushButton, "addFusePushButton")

        self.roomListView = self.findChild(QtGui.QListView, "roomListView")
        self.roomListView.setModel(self.model.get_room_table_model())
        self.roomListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #
        # self.socketListView = self.findChild(QtGui.QListView, "socketListView")
        # self.socketListView.setModel(self.model.get_socket_table_model())
        # self.socketListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #
        # self.fuseListView = self.findChild(QtGui.QListView, "fuseListView")
        # self.fuseListView.setModel(self.model.get_fuse_table_model())
        # self.fuseListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        # # self.roomListView.clicked.connect(self.roomListItemClicked)
        # self.fuseListView.doubleClicked.connect(self.fuseListItemDoubleClicked)
        self.roomListView.doubleClicked.connect(self.roomListItemDoubleClicked)
        # self.socketListView.doubleClicked.connect(self.socketListItemDoubleClicked)

        # self.roomListView.setStyleSheet(style)

        self.fuseTreeView = self.findChild(QtGui.QTreeView, "treeView")
        self.fuseTreeView.setModel(self.model.get_fuse_tree_item_model())
        self.fuseTreeView.doubleClicked.connect(self.treeViewDoubleClicked)

        self.addRoomPushbutton.clicked.connect(self.add_room_clicked)
        self.addSocketPushbutton.clicked.connect(self.add_socket_clicked)
        self.addFusePushbutton.clicked.connect(self.add_fuse_clicked)

        self.model.updated.connect(self.image_view.updateScene_)

        tabWidget.currentChanged.connect(self.model.updated)

        # self.model.cameraItemCreated.connect(self.range_view.updateScene_)
        # self.model.rangeFeatureCreated.connect(self.range_view.updateScene_)
        #
        # self._add_room_dialog = AddRoomDialog(model)

    def add_room_clicked(self):
        self.model.add_room()

    def add_socket_clicked(self):
        self.model.add_socket()

    def add_fuse_clicked(self):
        self.model.add_fuse()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def fuseListItemDoubleClicked(self, index):
        """
        Method called when user double-clicks on an entry in the camera-list to the right. Should open the
        camera_info_widget of the corresponding camera.
        :param index:
        :return:
        """
        idx= index.row()
        self.model.get_all_fuses()[idx].get_widget().show()


    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def socketListItemDoubleClicked(self, index):
        """
        Method called when user double-clicks on an entry in the camera-list to the right. Should open the
        camera_info_widget of the corresponding camera.
        :param index:
        :return:
        """
        idx = index.row()
        self.model.get_all_sockets()[idx].get_widget().show()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def roomListItemDoubleClicked(self, index):
        """
        Method called when user double-clicks on an entry in the camera-list to the right. Should open the
        camera_info_widget of the corresponding camera.
        :param index:
        :return:
        """
        idx= index.row()
        self.model.get_all_rooms()[idx].get_widget().show()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def treeViewDoubleClicked(self, index):
        widget = index.internalPointer().get_widget()
        if widget.isVisible():
            widget.hide()
        else:
            widget.show()
