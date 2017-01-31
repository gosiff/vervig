from PyQt4.QtCore import QPointF
from PyQt4 import QtCore
from PyQt4 import QtGui
from view.PTGraphicsItem import PTGraphicsItem
import math

__author__ = 'Fredrik Salovius'


class SwitchItem(PTGraphicsItem):
    """
    SwitchItem. Subclass of PTGraphicsItem, which is actually a QGraphicsObject. This is the draggable camera-icon
    seen in the RangeView scene. It visualises the Socket in the RangeView.
    Model: Socket
    """
    Type = QtGui.QGraphicsItem.UserType + 1

    deleteSocketAction = QtCore.pyqtSignal()

    def __init__(self):
        super(SwitchItem, self).__init__()

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

    def socket_polygon(self, width=50, height=20):
        """
        Create a polygon in the shape of a camera with the given dimensions.
        :param width: (optional) width of the polygon
        :param height: (optional) height of the polygon
        :return: QPolygonF object with the shape of a camera
        """
        points = [QPointF(-0.5*width, 0.6*height), QPointF(0.5*width, (0.6)*height),
                  QPointF((0.5)*width,-(0.6)*height), QPointF((-0.5)*width, -0.6*height)]
        polygon = QtGui.QPolygonF(points)
        return polygon

    # def ground_polygon(self):
    #     points = []
    #     socket_point = self.model.get_pos()
    #     a = self.rotation()
    #     transform = QtGui.QTransform().rotate(-a)
    #     points.append(transform.map(socket_point))
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
        # painter.setPen(QtCore.Qt.white)
        # painter.drawEllipse(-15, -15, 30, 30)

        painter.setPen(QtCore.Qt.black)
        socket_polygon = self.socket_polygon(5, 5)
        painter.drawPolygon(socket_polygon)

        font = painter.font()
        font.setPixelSize(10)
        painter.setPen(QtCore.Qt.red)
        painter.setFont(font)
        # painter.drawText(5, -5, str(self.model.get_model().get_all_sockets().index(self.model)))

        painter.drawText(5, -5, str(self.model.get_name()))

    def update(self, rect=QtCore.QRectF()):
        """
        Custom update method for the item.
        :param rect:
        :return:
        """
        super(SwitchItem, self).update(rect)

    def contextMenuEvent(self, event):
        """
        Display context menu when user clicks right mouse button on a SwitchItem.
        :param QContextMenuEvent:
        :return:
        """

        menu = QtGui.QMenu()

        deleteSocketAction = menu.addAction("Delete switch")
        deleteSocketAction.triggered.connect(self.deleteSocketAction)
        menu.exec_(event.screenPos())

    def setModel(self, model):
        super(SwitchItem, self).setModel(model)
        model.deleteRequested.connect(lambda: self.deleteSocketAction)

