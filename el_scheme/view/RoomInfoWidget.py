__author__ = 'Fredrik Salovius'
import ntpath
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
import re
from StringUtils import resource_path
import os


class RoomInfoWidget(QtGui.QWidget):
    """
    Model: Camera
    """

    # Signals
    room_name_changed = QtCore.pyqtSignal(str)
    pos_changed = QtCore.pyqtSignal(QtCore.QPointF)
    rotation_changed = QtCore.pyqtSignal(float)
    apply_data = QtCore.pyqtSignal(str, int, list, str)
    finished = QtCore.pyqtSignal()
    lock_room = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(RoomInfoWidget, self).__init__(parent)
        uic.loadUi(resource_path(os.path.join("ui", "room_info.ui")), self)

        button_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        button_box.clicked.connect(self.clicked)
        button_box.rejected.connect(self.reject)

        self.model = None
        self.proxy = None
        self.hide()

    def setModel(self, model):
        self.model = model
        model.set_widget(self)

        # Connect to signals emitted by model
        model.updated.connect(self.update)

        # Connect signals emitted by self to model
        self.apply_data.connect(model.set_properties_from_widget)
        self.finished.connect(self.hide)
        self.lock_room.connect(model.set_locked)

        self.update()

    def setProxy(self, proxy):
        self.proxy = proxy
        self.proxy.setZValue(4)
        self.proxy.setOpacity(0.8)
        self.proxy.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        self.update()
        self.hide()

    def update(self):
        self.findChild(QtGui.QLineEdit, "nameEdit").setText(self.model.get_name())
        self.findChild(QtGui.QLineEdit, "floorEdit").setText("{}".format(self.model.get_floor()))
        self.findChild(QtGui.QLineEdit, "numSocketsEdit").setText("{}".format(self.model.get_sockets()))
        self.findChild(QtGui.QLineEdit, "descriptionEdit").setText(self.model.get_description())
        # self.findChild(QtGui.QCheckBox, "lockCheckBox").setChecked(self.model.is_locked())

        if self.proxy:
            self.proxy.setPos(self.model.get_pos())

    # User pushed any button
    def clicked(self, button):
        button_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        if button_box.buttonRole(button) == QtGui.QDialogButtonBox.ApplyRole:
            self.apply()

    # User push Apply button
    def apply(self):

        name = self.findChild(QtGui.QLineEdit, "nameEdit").text()
        floor = self.findChild(QtGui.QLineEdit, "floorEdit").text()
        num_sockets = self.findChild(QtGui.QLineEdit, "numSocketsEdit").text()
        description = self.findChild(QtGui.QLineEdit, "descriptionEdit").text()

        # self.lock_camera.emit(self.findChild(QtGui.QCheckBox, "lockCheckBox").isChecked())
        self.apply_data.emit(name, int(floor), [], description)

    # User push Close button
    def reject(self):
        self.finished.emit()

    def hide(self):
        if self.proxy:
            self.proxy.hide()

    def show(self):
        if self.proxy:
            self.proxy.show()
