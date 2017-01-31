__author__ = 'Fredrik Salovius'
import ntpath
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
import re
from StringUtils import resource_path
import os


class FuseInfoWidget(QtGui.QWidget):
    """
    Model: Camera
    """

    # Signals
    fuse_name_changed = QtCore.pyqtSignal(str)
    pos_changed = QtCore.pyqtSignal(QtCore.QPointF)
    # rotation_changed = QtCore.pyqtSignal(float)
    apply_data = QtCore.pyqtSignal(int, int, int)
    finished = QtCore.pyqtSignal()
    # lock_room = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(FuseInfoWidget, self).__init__(parent)
        uic.loadUi(resource_path(os.path.join("ui", "fuse_info.ui")), self)

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
        # self.lock_room.connect(model.set_locked)

        self.update()

    def setProxy(self, proxy):
        self.proxy = proxy
        self.proxy.setZValue(4)
        self.proxy.setOpacity(0.8)
        self.proxy.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        self.update()
        self.hide()

    def update(self):
        _id = self.model.get_fuse_id()
        self.findChild(QtGui.QLineEdit, "fuseIdLineEdit").setText(str(self.model.get_fuse_id()))
        self.findChild(QtGui.QLineEdit, "nominalCurrentLineEdit").setText(str(self.model.get_nominal_current()))
        self.findChild(QtGui.QLineEdit, "cableDimensionLineEdit").setText(str(self.model.get_cable_dimension()))


        socketsListWidget = self.findChild(QtGui.QListWidget, 'socketsListWidget')
        socketsListWidget.clear()
        child_sockets = self.model.get_all_children()
        all_sockets = self.model.get_model().get_all_sockets()
        for child_socket in child_sockets:
            # my_str = str(all_sockets.index(child_socket))
            # my_str = .get_name()
            socketsListWidget.addItem(QtGui.QListWidgetItem(child_socket.get_name()))

        if self.proxy:
            self.proxy.setPos(self.model.get_pos())

    # User pushed any button
    def clicked(self, button):
        button_box = self.findChild(QtGui.QDialogButtonBox, "buttonBox")
        if button_box.buttonRole(button) == QtGui.QDialogButtonBox.ApplyRole:
            self.apply()

    # User push Apply button
    def apply(self):

        _nominal_current = self.findChild(QtGui.QLineEdit, "nominalCurrentLineEdit").text()
        _dimension = self.findChild(QtGui.QLineEdit, "cableDimensionLineEdit").text()
        _id = self.findChild(QtGui.QLineEdit, "fuseIdLineEdit").text()
        try:
            _nominal_current = int(_nominal_current)
            _dimension = int(_dimension)
            _id = int(_id)
            fuse_id_list = [obj.get_fuse_id() for obj in self.model.get_model().get_all_fuses()]
            if _id in fuse_id_list:
                print 'id [{_id}] already taken '.format(_id=_id)
                _id = self.model.get_fuse_id()
        except:
            _id = self.model.get_fuse_id()
            _nominal_current = self.model.get_nominal_current()
            _dimension = self.model.get_cable_dimension()


        # self.lock_camera.emit(self.findChild(QtGui.QCheckBox, "lockCheckBox").isChecked())
        self.apply_data.emit(_id, _nominal_current, _dimension)

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

