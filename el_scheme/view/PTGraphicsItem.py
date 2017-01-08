from PyQt4 import QtCore
from PyQt4 import QtGui

__author__ = 'Fredrik'


class PTGraphicsItem(QtGui.QGraphicsObject):
    """
    PTGraphicsItem. Parent-class for GraphicsObjects seen in the RangeView scene (Targets and Cameras for now).
    Defines some non-default behaviour that's common for both TargetItems and CameraItems, such as the update(),
    __init__(), setModel(), mouseReleaseEvent() and mouseDoubleClickEvent() methods.
    """
    Type = QtGui.QGraphicsItem.UserType + 1

    # Signals
    double_clicked = QtCore.pyqtSignal()  # User double-clicked on the item
    moved = QtCore.pyqtSignal(QtCore.QPointF)  # User moved item around
    press = QtCore.pyqtSignal()  # User press mouse button over an item

    def __init__(self):
        super(PTGraphicsItem, self).__init__()
        self.model = None
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)
        self._is_moving = False

    def setModel(self, model):
        """
        Set the model defining the state of the PTGraphicsItem.
        :param model: The CameraModel or TargetModel to associate with this item.
        :return:
        """
        self.model = model

        # Connect to signals emitted by model
        model.updated.connect(self.update)

        # Connect signals emitted by CameraItem
        self.moved.connect(model.set_pos)
        self.update()

    def boundingRect(self):
        """
        Returns the painted area of the item.
        :return: The area to be painted in the scene as a QRectF
        """
        return QtCore.QRectF(-100, -100, 200, 200)

    def shape(self):
        """
        Return the draggable area of the item.
        :return: The draggable area as a QPainterPath
        """
        path = QtGui.QPainterPath()
        path.addEllipse(-15, -15, 30, 30)
        return path

    def update(self, rect=QtCore.QRectF()):
        super(PTGraphicsItem, self).update(rect)
        self.setPos(self.model.get_pos())

    def itemChange(self, change, value):
        return super(PTGraphicsItem, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super(PTGraphicsItem, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Event triggered when a mouse button is released.
        :param event: The triggering event.
        :return:
        """
        self.update()
        super(PTGraphicsItem, self).mouseReleaseEvent(event)
        if self.flags() & QtGui.QGraphicsItem.ItemIsMovable and self._is_moving:
            t = QtGui.QTransform()
            self.moved.emit(event.scenePos() - event.pos()*t.rotate(self.rotation()))  # Let the item emit the position of itself in the scene
            self._is_moving = False

    def mouseMoveEvent(self, event):
        self.update(self.boundingRect())
        self._is_moving = True
        super(PTGraphicsItem, self).mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        """
        Event triggered when user double-clicks the left mouse button.
        :param event: The triggering event,
        :return:
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.update()
            self.double_clicked.emit()
