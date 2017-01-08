from PIL import Image

__author__ = 'Fredrik Salovius'
from PyQt4 import QtCore
from PyQt4 import QtGui
from view.SocketItem import SocketItem
from view.SocketInfoWidget import SocketInfoWidget
from view.RoomItem import RoomItem
from view.RoomInfoWidget import RoomInfoWidget
from view.ZoomableGraphicsView import ZoomableGraphicsView


class HouseImageView(ZoomableGraphicsView):
    """
    RangeView. The top-down view of the range, displayed in the first tab of the Overview view.
    Contains a GraphicsScene containing CameraItems, TargetItems, CameraInfoWidgets and TargetInfoWidgets.
    Model: Range
    """

    error_message = QtCore.pyqtSignal(str)

    def __init__(self, model, parent=None):
        super(HouseImageView, self).__init__(parent)
        self.model = model

        self.scene().addSocketAction = lambda pos: self.model.add_socket(pos)
        self.scene().addRoomAction = lambda pos: self.model.add_room(pos)
        self.scene().setImageAction.connect(self._open_background_image_dialog)

        self.background_image = QtGui.QImage()
        self.setBackgroundBrush(QtGui.QColor(50, 50, 50))

        self.show()
        self.updateScene_()

    def _setup_background(self):
        """
        Set the loaded background image as background pixmap for the scene.
        :return:
        """
        self.background_image = QtGui.QImage()
        data = self.model.get_background_image_data()
        self.background_image.loadFromData(data,'PNG')
        self.scene().addPixmap(QtGui.QPixmap.fromImage(self.background_image))
        self.fitInView(QtCore.QRectF(self.background_image.rect()), QtCore.Qt.KeepAspectRatio)

    def _open_background_image_dialog(self):
        """
        Open a file dialog for letting the user choose a background image
        :return:
        """
        new_background_image_file = QtGui.QFileDialog.getOpenFileName(parent=None, caption="Open background image file",
                                                           directory="resources",
                                                           filter="Image files (*.png *.jpg *.bmp)")


        if new_background_image_file:
            # im = Image.open(new_background_image_file)
            # bytes = Image.toBytes()
            self.model.set_background_image(new_background_image_file)
            img = QtGui.QImage()
            img.load(new_background_image_file)
            data = QtCore.QByteArray()
            buf = QtCore.QBuffer(data)
            img.save(buf, 'PNG')
            self.model.set_background_image_data(data)
            self.updateScene_()

    def resizeEvent(self, QResizeEvent):
        self.fitInView(QtCore.QRectF(self.background_image.rect()), QtCore.Qt.KeepAspectRatio)

    @QtCore.pyqtSlot(RoomItem)
    def updateScene_(self):
        """
        Update the scene by first clearing it, and then add everything it should contain.
        :return:
        """
        self.scene().clear()

        self._setup_background()
        self._add_sockets()
        self._add_rooms()

    def _add_socket(self, socket_model):
        """
        Create a new CameraItem and CameraInfoWidget and add them to the scene.
        :param camera_model: CameraModel to associate with the CameraItem and CameraInfoWidget.
        :return:
        """

        # Create a new CameraItem and set the model
        socket_item = SocketItem()
        socket_item.setModel(socket_model)

        # Create a new CameraInfoWidget and set the model
        socket_widget = SocketInfoWidget()
        socket_widget.setModel(socket_model)

        socket_item.double_clicked.connect(socket_widget.show)
        socket_item.deleteSocketAction.connect(socket_model.prepare_for_deletion)

        self.scene().addItem(socket_item)
        proxy = self.scene().addWidget(socket_widget)
        socket_widget.setProxy(proxy)

    def _add_sockets(self):
        """
        Add all cameras in the RangeModel to the scene.
        :return:
        """
        sockets = self.model.get_all_sockets()

        for socket in sockets:
            self._add_socket(socket)

    def _add_room(self, room_model):
        """
        Create a new TargetItem and TargetInfoWidget and add them to the scene
        :param room_model: TargetModel to associate with the TargetItem and TargetInfoWidget.
        :return:
        """

        # Create a new TargetItem and set the model
        room_item = RoomItem()
        room_item.setModel(room_model)

        # Create a new TargetInfoWidget and set the model
        room_widget = RoomInfoWidget()
        room_widget.setModel(room_model)

        # Connect signals emitted by TargetItem
        # room_item.moved.connect(room_model.set_pos)
        room_item.double_clicked.connect(room_widget.show)
        room_item.deleteRoomAction.connect(room_model.prepare_for_deletion)

        # Connect signals emitted by TargetInfoWidget

        room_widget.finished.connect(room_widget.hide)

        self.scene().addItem(room_item)
        room_item.update()
        proxy = self.scene().addWidget(room_widget)
        room_widget.setProxy(proxy)

    def _add_rooms(self):
        """
        Add all targets in the RangeModel to the scene.
        :return:
        """
        rooms = self.model.get_all_rooms()

        for room in rooms:
            self._add_room(room)

