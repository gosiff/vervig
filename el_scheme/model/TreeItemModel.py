from model.socket import Socket

__author__ = 'Fredrik Salovius'

# How it would look like:
# fuse id 1
#     -  socket id    | room name
#     -  socket id    | room name
#     -  socket id    | room name
#     -  socket id    | room name
# fuse id 2
#     -  socket id    | room name
#     -  socket id    | room name
#     -  socket id    | room name
#     -  socket id    | room name

# alternative:
#
# Fuse id 1
#   - room id
#       - socket id
#       - socket id
#       - socket id
#   - room id
#       - socket id
#

from PyQt4 import QtGui, QtCore

class CustomNode(object):
    def __init__(self, data):
        self.model = data
        self._column_count = 3
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column):
        if isinstance(self.model, Socket):
            if column == 0:
                return self.model.get_id()
            elif column == 1:
                return self.model.get_model().get_room_name_by_id(self.model.get_room_id())
        elif self.model is not None:
            return 'Fuse ' + str(self.model)

    def columnCount(self):
        return self._column_count

    def childCount(self):
        return len(self._children)

    def child(self, row):
        if row >= 0 and row < self.childCount():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, child):
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent):
        super(TreeModel, self).__init__(parent)
        self._root = CustomNode(None)
        self.parent = parent
        
    def rowCount(self, index):
        if index.isValid():
            return index.internalPointer().childCount()
        return self._root.childCount()

    def addNewChild(self, node):
        self._root.addChild(node)

    def addChild(self, node, parent):
        if not parent or not parent.isValid():
            _parent = self._root
        else:
            _parent = parent.internalPointer()
        _parent.addChild(node)

    def index(self, row, column, parent=None):
        if not parent or not parent.isValid():
            _parent = self._root
        else:
            _parent = parent.internalPointer()

        if not QtCore.QAbstractItemModel.hasIndex(self, row, column, parent):
            return QtCore.QModelIndex()

        child = _parent.child(row)
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QtCore.QModelIndex()

    def columnCount(self, index):
        if index.isValid():
            return index.internalPointer().columnCount()
        return self._root.childCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return node.data(index.column())
        return None
