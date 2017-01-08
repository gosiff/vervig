from PyQt4 import QtCore
from PyQt4 import QtGui

__author__ = 'Fredrik Salovius'


class RoomTableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent):
        super(RoomTableModel, self).__init__(parent)
        self.header = ["Name", "ID", "Description", "Floor", "Sockets", "Delete"]
        self.parent = parent
        self.parent.updated.connect(self.reset)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.parent.get_all_rooms())

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 8

    def getId(self, index):
        model = self.parent.get_all_rooms()[index.row()]
        return model.get_id()

    def data(self, index, role=QtCore.Qt.DisplayRole):

        room_model = self.parent.get_all_rooms()[index.row()]
        if not index.isValid():
            return
        elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return QtCore.QVariant(room_model.get_name())
            elif index.column() == 1:
                return QtCore.QVariant(room_model.get_id())
            elif index.column() == 2:
                return QtCore.QVariant(room_model.get_description())
            elif index.column() == 3:
                return QtCore.QVariant(room_model.get_floor())
            elif index.column() == 4:
                return QtCore.QVariant(room_model.get_sockets())
        return QtCore.QVariant()

    def setData(self, index, value, int_role=None):
        # self.header = ["Name", "ID", "Description", "Floor", "Sockets", "Delete"]
        if int_role != QtCore.Qt.EditRole:
            return False
        room_model = self.parent.get_all_rooms()[index.row()]

        if index.column() == 0:
            room_model.set_name(value.toString())
        elif index.column() == 2:
            room_model.set_description(value.toString())
        elif index.column() == 3:
            room_model.set_floor(int(value.toString()))

        return True

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.header[section]

        return QtCore.QVariant()

    @QtCore.pyqtSlot()
    def updateAll(self):
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount(), self.columnCount()))
