__author__ = 'Fredrik Salovius'
import ntpath
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
import re
from StringUtils import resource_path
import os


class LampOutletInfoWidget(QtGui.QWidget):
    """
    Model: Camera
    """

    # Signals
    # camera_name_changed = QtCore.pyqtSignal(str)
    # camera_pos_changed = QtCore.pyqtSignal(QtCore.QPointF)
    # camera_rotation_changed = QtCore.pyqtSignal(float)
    # camera_mac_changed = QtCore.pyqtSignal(str)
    # apply_data = QtCore.pyqtSignal(str, str, float, float, float, float, float, float, str)
    # apply_calibration = QtCore.pyqtSignal(str, str)
    finished = QtCore.pyqtSignal()
    # selected_intrinsics = QtCore.pyqtSignal(str)
    lock_socket = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(LampOutletInfoWidget, self).__init__(parent)
        uic.loadUi(resource_path(os.path.join("ui", "lamp_outlet_info.ui")), self)

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
        self.finished.connect(self.hide)

        self.update()

    def setProxy(self, proxy):
        self.proxy = proxy
        self.proxy.setZValue(4)
        self.proxy.setOpacity(0.8)
        self.proxy.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        self.update()
        self.hide()

    def update(self):
        fuse_id_cb = self.findChild(QtGui.QComboBox, 'fuseIdComboBox')
        fuse_id_cb.clear()
        fuse_id_cb.addItem('-- Availible fuse --')
        item_selected = 0
        iter = 0
        for fuse in self.model.get_model().get_all_fuses():
            iter += 1
            fuse_id_cb.addItem(str(fuse.get_fuse_id()))
            if fuse.get_fuse_id() == self.model.get_fuse().get_fuse_id():
                item_selected = iter
        fuse_id_cb.setCurrentIndex(item_selected)

        room_cb = self.findChild(QtGui.QComboBox, 'roomComboBox')
        room_cb.clear()
        room_cb.addItem('-- Availible rooms --')
        item_selected = 0
        iter = 0
        for room in self.model.get_model().get_all_rooms():
            iter += 1
            item_name = room.get_name() + ' (' + str(room.get_id()) + ')'
            room_cb.addItem(item_name)
            if room.get_id() == self.model.get_room_id():
                item_selected = iter
        room_cb.setCurrentIndex(item_selected)

        switch_list = self.findChild(QtGui.QListWidget, 'switchListWidget')
        switch_list.clear()

        for sw  in self.model.get_all_children():
            switch_name = sw.get_name()
            switch_list.addItem(switch_name)

        if self.proxy:
            self.proxy.setPos(self.model.get_pos())

    # User pushed any button
    def clicked(self, button):
        button_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        if button_box.buttonRole(button) == QtGui.QDialogButtonBox.ApplyRole:
            self.apply()

    # User push Apply button
    def apply(self):
        fuse_cb_text = self.findChild(QtGui.QComboBox, 'fuseIdComboBox').currentText()
        room_cb_text = self.findChild(QtGui.QComboBox, 'roomComboBox').currentText()
        try:
            room_id = int(room_cb_text[room_cb_text.find('(')+1:-1])
        except:
            room_id = None
        self.model.set_room_id(room_id)
        for fuse in self.model.get_model().get_all_fuses():
            if str(fuse.get_fuse_id()) == fuse_cb_text:
                self.model.get_fuse().updated.emit()
                fuse.addChild(self.model)
                break

        outlets = self.findChild(QtGui.QSpinBox, 'outletSpinBox').value()
        self.model.set_outlets(outlets)

    # User push Close button
    def reject(self):
        self.finished.emit()

    def hide(self):
        if self.proxy:
            self.proxy.hide()

    def show(self):
        if self.proxy:
            self.update()
            self.proxy.show()
