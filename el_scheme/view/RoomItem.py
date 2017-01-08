from PyQt4.QtCore import QPointF
from PyQt4 import QtCore
from PyQt4 import QtGui
from view.PTGraphicsItem import PTGraphicsItem
import math

__author__ = 'Fredrik Salovius'


class RoomItem(PTGraphicsItem):
    """
    CameraItem. Subclass of PTGraphicsItem, which is actually a QGraphicsObject. This is the draggable camera-icon
    seen in the RangeView scene. It visualises the Camera in the RangeView.
    Model: Camera
    """
    Type = QtGui.QGraphicsItem.UserType + 1

    deleteRoomAction = QtCore.pyqtSignal()

    def __init__(self):
        super(RoomItem, self).__init__()

        self.model = None

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)

    def boundingRect(self):
        """
        Defines the rendering-area of the item in the view.
        :return:
        """
        return QtCore.QRectF(-1000, -1000, 2000, 2000)

    def room_polygon(self, width=50, height=20):
        """
        Create a polygon in the shape of a camera with the given dimensions.
        :param width: (optional) width of the polygon
        :param height: (optional) height of the polygon
        :return: QPolygonF object with the shape of a camera
        """

        points = self.model.bounding_box
        polygon = QtGui.QPolygonF(points)
        return polygon

    # def ground_polygon(self):
    #     points = []
    #
    #     room_point = self.model.get_pos()
    #     a = self.rotation()
    #     transform = QtGui.QTransform().rotate(-a)
    #     points.append(transform.map(room_point)
    #
    #     return QtGui.QPolygonF(points)

    def paint(self, painter, option, widget):
        """
        Paints the camera item onto the scene.
        :param painter: painter object used for painting.
        :param option:
        :param widget:
        :return:
        """

        painter.setPen(QtCore.Qt.white)
        painter.drawEllipse(-15, -15, 30, 30)

        font = painter.font()
        font.setPixelSize(15)
        if self.model.is_selected():
            painter.setPen(QtCore.Qt.red)
        else:
            painter.setPen(QtCore.Qt.blue)
        font.setStyleHint(QtGui.QFont.TypeWriter)
        font.setFamily("Courier Code")
        painter.setFont(font)
        metrics = QtGui.QFontMetrics(font)
        name = self.model.get_name()
        text_length = metrics.width(name)
        text_height = metrics.height()

        bounding_rect = metrics.boundingRect(name)
        bounding_rect.moveTo(-text_length/2, -text_height/3)
        painter.drawRects(bounding_rect)
        painter.drawText(-text_length/2, text_height/2, str(name))

    def update(self, rect=QtCore.QRectF()):
        """
        Custom update method for the item.
        :param rect:
        :return:
        """
        super(RoomItem, self).update(rect)

    def contextMenuEvent(self, event):
        """
        Display context menu when user clicks right mouse button on a CameraItem.
        :param QContextMenuEvent:
        :return:
        """

        menu = QtGui.QMenu()

        deleteRoomAction = menu.addAction("Delete room")
        deleteRoomAction.triggered.connect(self.deleteRoomAction)
        menu.exec_(event.screenPos())

    def setModel(self, model):
        super(RoomItem, self).setModel(model)
        model.deleteRequested.connect(lambda: self.deleteRoomAction)

