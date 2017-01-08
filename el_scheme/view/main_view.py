from view.image_view import HouseImageView

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
        uic.loadUi(resource_path(os.path.join("ui", "mainview_widget.ui")), self)
        tabWidget = self.findChild(QtGui.QTabWidget, "tabWidget")
        self.image_view = HouseImageView(self.model)
        tabWidget.addTab(self.image_view, "Overview")
        self.loadImagePushbutton= self.findChild(QtGui.QPushButton, "loadImagePushButton")
        self.addRoomPushbutton= self.findChild(QtGui.QPushButton, "addRoomPushButton")
        self.addSocketPushbutton= self.findChild(QtGui.QPushButton, "addSocketPushButton")
        self.roomListView= self.findChild(QtGui.QListView, "roomListView")
        self.roomListView.setModel(self.model.get_room_table_model())
        self.roomListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        # self.roomListView.clicked.connect(self.cameraListItemClicked)
        # self.roomListView.doubleClicked.connect(self.cameraListItemDoubleClicked)
        self.roomListView.setStyleSheet(style)
        self.fuseTreeView = self.findChild(QtGui.QTreeView, "treeView")
        self.fuseTreeView.setModel(self.model.get_fuse_tree_item_model())
        self.addRoomPushbutton.clicked.connect(self.add_room_clicked)

        self.model.updated.connect(self.image_view.updateScene_)
        # self.model.cameraItemCreated.connect(self.range_view.updateScene_)
        # self.model.rangeFeatureCreated.connect(self.range_view.updateScene_)
        #
        self._add_room_dialog = AddRoomDialog(model)


    def add_room_clicked(self):
        self._add_room_dialog.show()
