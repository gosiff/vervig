from PyQt4 import QtCore
from PyQt4 import QtGui
from view.PTGraphicsScene import PTGraphicsScene

__author__ = 'Fredrik'


class ZoomableGraphicsView(QtGui.QGraphicsView):
    """
    RangeView. The top-down view of the range, displayed in the first tab of the Overview view.
    Contains a GraphicsScene containing CameraItems, TargetItems, CameraInfoWidgets and TargetInfoWidgets.
    Model: Range
    """

    error_message = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ZoomableGraphicsView, self).__init__(parent)
        scene = PTGraphicsScene()
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.setScene(scene)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.h11 = 1.0
        self.h22 = 1.0

    def wheelEvent(self, QWheelEvent):
        # Typical Calculations (Ref Qt Doc)
        degrees = QWheelEvent.delta() / 8
        steps = degrees / 15

        # Declare below as class member vars and set default values as below

        scale_factor = 1.25  # How fast we zoom
        min_factor = 0.75
        max_factor = 10.0

        if steps > 0:
            self.h11 = self.h11 if (self.h11 >= max_factor) else (self.h11 * scale_factor)
            self.h22 = self.h22 if (self.h22 >= max_factor) else (self.h22 * scale_factor)
        else:
            self.h11 = self.h11 if (self.h11 <= min_factor) else (self.h11 / scale_factor)
            self.h22 = self.h22 if (self.h22 <= min_factor) else (self.h22 / scale_factor)

        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setTransform(QtGui.QTransform(self.h11, 0, 0, self.h22, 0, 0))
