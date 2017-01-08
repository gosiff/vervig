from PyQt4 import QtGui
from PyQt4 import QtCore
from view.PTGraphicsItem import PTGraphicsItem

__author__ = 'Fredrik'


class PTGraphicsScene(QtGui.QGraphicsScene):
    """
    PTGraphicsScene. Inherits from QGraphicsScene. Allows us to catch events in a customized fashion.
    """
    # addCameraAction(QtCore.QPoint) defined in RangeView
    # addTargetAction(QtCore.QPoint) defined in RangeView
    setImageAction = QtCore.pyqtSignal()

    def __init__(self):
        super(PTGraphicsScene, self).__init__()

    def contextMenuEvent(self, QContextMenuEvent):
        """
        Display context menu when user clicks right mouse button in the graphicsview.
        :param QContextMenuEvent:
        :return:
        """
        # super(PTGraphicsScene, self).contextMenuEvent(QContextMenuEvent)

        # we check if clicked_item is PTGraphicsItem (which has its own menu)
        # so we don't spawn two menus with one click.
        clicked_item = self.itemAt(QContextMenuEvent.scenePos())
        if isinstance(clicked_item, PTGraphicsItem):
            super(PTGraphicsScene, self).contextMenuEvent(QContextMenuEvent)
        else:
            menu = QtGui.QMenu()
            set_image_menu_action = menu.addAction("Set background image")
            add_socket_menu_action = menu.addAction("Add socket")
            add_room_menu_action = menu.addAction("Add room")
            set_image_menu_action.triggered.connect(self.setImageAction)
            add_socket_menu_action.triggered.connect(lambda: self.addSocketAction(QContextMenuEvent.scenePos()))
            add_room_menu_action.triggered.connect(lambda: self.addRoomAction(QContextMenuEvent.scenePos()))

            menu.exec_(QContextMenuEvent.screenPos())


class PTGraphicsSceneTE(QtGui.QGraphicsScene):
    """
    PTGraphicsSceneTE. Inherits from QGraphicsScene. Intended for use in TargetEditor
    """

    leftMousePressedOnBackground = QtCore.pyqtSignal()
    rightMousePressedOnBackground = QtCore.pyqtSignal()
    leftMouseReleasedOnBackground = QtCore.pyqtSignal()

    def __init__(self):
        super(PTGraphicsSceneTE, self).__init__()

    def mousePressEvent(self, QMouseEvent):
        """
        Switch background image if user clicks mouse inside graphicsView, but not if clicked on an item
        :param QMouseEvent:
        :return:
        """
        if self.itemAt(QMouseEvent.scenePos()) is None:
            super(PTGraphicsSceneTE, self).mousePressEvent(QMouseEvent)
        elif self.itemAt(QMouseEvent.scenePos()).type() == QtGui.QGraphicsPixmapItem().type():
            if QMouseEvent.button() == QtCore.Qt.LeftButton:
                self.leftMousePressedOnBackground.emit()
                super(PTGraphicsSceneTE, self).mousePressEvent(QMouseEvent)
            elif QMouseEvent.button() == QtCore.Qt.RightButton:
                self.rightMousePressedOnBackground.emit()
                QMouseEvent.accept()
        else:
            if QMouseEvent.button() == QtCore.Qt.LeftButton:
                super(PTGraphicsSceneTE, self).mousePressEvent(QMouseEvent)
            elif QMouseEvent.button() == QtCore.Qt.RightButton:
                QMouseEvent.accept()

    def mouseReleaseEvent(self, QGraphicsSceneMouseEvent):
        super(PTGraphicsSceneTE, self).mouseReleaseEvent(QGraphicsSceneMouseEvent)
        self.leftMouseReleasedOnBackground.emit()
