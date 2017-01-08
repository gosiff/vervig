__author__ = 'Fredrik Salovius'
from PyQt4 import QtGui
from PyQt4 import uic
from StringUtils import resource_path
import os


class AddRoomDialog(QtGui.QDialog):
    def __init__(self, model):
        super(AddRoomDialog, self).__init__()
        uic.loadUi(resource_path(os.path.join("ui", "add_room_dialog.ui")), self)
        self.model = model

        self.ok_button = self.findChild(QtGui.QPushButton, "okButton")
        self.floorSpinBox = self.findChild(QtGui.QSpinBox, "floorSpinBox")
        self.socketsSpinBox = self.findChild(QtGui.QSpinBox, "socketSpinBox")
        self.descriptionTextBox = self.findChild(QtGui.QTextEdit, "descriptionTextEdit")
        self.nameTextBox = self.findChild(QtGui.QLineEdit, 'nameLineEdit')
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.description = ''
        # self.descriptionTextBox.textChanged.connect

    def on_ok_clicked(self):
        description = self.descriptionTextBox.toPlainText()
        self.model.add_room(self.nameTextBox.text(), description, self.floorSpinBox.value(), self.socketsSpinBox.value())
        self.hide()

    def show(self):
        super(AddRoomDialog, self).show()
        self.floorSpinBox.setValue(0)
        self.socketsSpinBox.setValue(0)
        self.descriptionTextBox.clear()
        self.nameTextBox.clear()


    # def setDescription(self):
    #     self.description
