from PyQt4.QtCore import QPointF
from PyQt4 import QtCore
from PyQt4 import QtGui
from view.PTGraphicsItem import PTGraphicsItem
import math

__author__ = 'Fredrik Salovius'


class FuseItem(PTGraphicsItem):
    """
    CameraItem. Subclass of PTGraphicsItem, which is actually a QGraphicsObject. This is the draggable camera-icon
    seen in the RangeView scene. It visualises the Camera in the RangeView.
    Model: Camera
    """
    Type = QtGui.QGraphicsItem.UserType + 1

    deleteFuseAction = QtCore.pyqtSignal()

    def __init__(self):
        super(FuseItem, self).__init__()

        self.model = None

        # self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        # self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(100)
        self.setVisible(False)

    def boundingRect(self):
        """
        Defines the rendering-area of the item in the view.
        :return:
        """
        return QtCore.QRectF(-10, -10, 20, 20)


    def paint(self, painter, option, widget):
        """
        Paints the camera item onto the scene.
        :param painter: painter object used for painting.
        :param option:
        :param widget:
        :return:
        """
        painter.setPen(QtGui.QPen(QtCore.Qt.darkGray, 2, QtCore.Qt.SolidLine))
        size = 8
        painter.drawEllipse(-size, -size, 2 * size, 2 * size)

        # font = painter.font()
        # font.setPixelSize(15)
        painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine))

        painter.setBrush(QtCore.Qt.gray)
        size = 4
        painter.drawEllipse(-size, -size, 2 * size, 2 * size)



        # font.setStyleHint(QtGui.QFont.TypeWriter)
        # font.setFamily("Courier Code")
        # painter.setFont(font)
        # metrics = QtGui.QFontMetrics(font)
        # name = self.model.get_name()
        # text_length = metrics.width(name)
        # text_height = metrics.height()

        # bounding_rect = metrics.boundingRect(name)
        # bounding_rect.moveTo(-text_length/2, -text_height/3)
        # painter.drawRects(bounding_rect)
        # painter.drawText(-text_length/2, text_height/2, str(name))

    def update(self, rect=QtCore.QRectF()):
        """
        Custom update method for the item.
        :param rect:
        :return:
        """
        super(FuseItem, self).update(rect)

    def contextMenuEvent(self, event):
        """
        Display context menu when user clicks right mouse button on a CameraItem.
        :param QContextMenuEvent:
        :return:
        """

        menu = QtGui.QMenu()

        deleteFuseAction = menu.addAction("Delete fuse")
        deleteFuseAction.triggered.connect(self.deleteFuseAction)
        menu.exec_(event.screenPos())

    def setModel(self, model):
        super(FuseItem, self).setModel(model)
        model.deleteRequested.connect(lambda: self.deleteFuseAction)

