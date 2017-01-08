__author__ = 'Fredrik Salovius'
# coding=utf8
from PyQt4 import QtCore
from Commands import GenericSetCommand
import copy

class HouseFeature(QtCore.QObject):
    # Signals
    updated = QtCore.pyqtSignal()  # Emitted whenever the model has been changed, and the item should be updated.

    def __init__(self, name, description=None):
        super(HouseFeature, self).__init__()
        self._house = None
        self._name = name
        self._description = description if description is not None else ""
        self._graphics_item = None
        self._graphics_widget = None

    def __getstate__(self):
        """
        Return the __dict__ of the object, stripped from contents that doesn't need serialization.
        :return: dict
        """

        d = copy.copy(self.__dict__)
        # Do not save references to view
        del d['_graphics_item']
        del d['_graphics_widget']

        return d

    def __setstate__(self, state):
        """
        Define unserialization of object from the state-dict.
        :param state:
        :return:
        """

        """# Support adding a new member not previously defined in the class
        if 'new_member' not in state:
            self.new_member = "new value"
        self.__dict__.update(state)"""

        """ # Support removing old members not in new version of class
        if 'old_member' in state:
            # If you want: do something with the old member
            del state['old_member']
        self.__dict__.update(state) """

        # Re-create pickled objects
        self.__init__("")
        self.__dict__.update(state)

    def get_id(self):
        for k, v in self.get_model().get_features().iteritems():
            if v is self:
                return k

        raise KeyError("Feature not found in Range._features.")

    def set_model(self, new_house):
        """
        Sets a reference to the associated Range object
        :param new_house: Range object
        """
        self._house = new_house
        self.updated.emit()

    def get_model(self):
        return self._house

    def _get_coord(self, index):
        NotImplementedError('Abstract method. Implement in subclass')

    def _set_coord(self, c, index):
        NotImplementedError('Abstract method. Implement in subclass')

    def get_x(self):
        """
        Returns the x-coordinate of the camera's 3D-position on the Range.
        :return: float x
        """
        return self._get_coord(0)

    def _set_x(self, x):
        """
        Sets the x-coordinate of the camera's 3D-position on the Range.
        :param x: float
        :return:
        """
        self._set_coord(x, 0)
        self.updated.emit()

    def set_x(self, x):
        """
        Sets the x-coordinate of the camera's 3D-position on the Range.
        :param x: float
        :return:
        """
        cmd = GenericSetCommand(self._set_x, self.get_x, x)
        self.get_house().get_invoker().store_and_execute(cmd)

    def get_y(self):
        """
        Returns the y-coordinate of the camera's 3D-position on the Range.
        :return: float y
        """
        return self._get_coord(1)

    def _set_y(self, y):
        """
        Sets the y-coordinate of the camera's 3D-position on the Range.
        :param y: float
        :return:
        """
        self._set_coord(y, 1)
        self.updated.emit()

    def set_y(self, y):
        """
        Sets the y-coordinate of the camera's 3D-position on the Range.
        :param y: float
        :return:
        """
        cmd = GenericSetCommand(self._set_y, self.get_y, y)
        self.get_house().get_invoker().store_and_execute(cmd)

    def get_z(self):
        """
        Returns the z-coordinate of the camera's 3D-position on the Range.
        :return: float z
        """
        return self._get_coord(2)

    def _set_z(self, z):
        """
        Sets the z-coordinate of the camera's 3D-position on the Range.
        :param z: float
        :return:
        """
        self._set_coord(z, 2)
        self.updated.emit()

    def set_z(self, z):
        """
        Sets the z-coordinate of the camera's 3D-position on the Range.
        :param z: float
        :return:
        """
        cmd = GenericSetCommand(self._set_z, self.get_z, z)
        self.get_house().get_invoker().store_and_execute(cmd)

    def _get_house_scale_factor(self):
        """
        Returns the scale factor of the associated Range object
        """
        return self.get_house().get_scale() if self.get_house() is not None else None

    def get_feature_type(self):
        """
        Abstract method returning type of range feature as a string.
        """
        raise NotImplementedError("Abstract method. Implement in subclass.")

    def get_name(self):
        return self._name

    def _set_name(self, name):
        """
        Sets the name of the feature.
        :param name: str
        :return:
        """
        self._name = name
        self.updated.emit()

    def set_name(self, name):
        """
        Sets the name of the feature.
        :param name: str
        :return:
        """
        cmd = GenericSetCommand(self._set_name, self.get_name, name)
        self.get_house().get_invoker().store_and_execute(cmd)

    def get_description(self):
        return self._description

    def _set_description(self, description):
        self._description = description
        self.updated.emit()

    def set_description(self, description):
        cmd = GenericSetCommand(self._set_description, self.get_description, description)
        self.get_house().get_invoker().store_and_execute(cmd)

    def get_pos(self):
        """
        Returns the image position of the feature i screen coordinates (pixels)
        :return: QtCore.QPosF(x,y)
        """
        raise NotImplementedError('Abstract method. Implement in subclass')

    def set_pos(self, new_pos):
        """
        new_pos is given in screen coordinates (pixels)
        :param new_pos: QtCore.QPointF(x, y)
        :return:
        """
        raise NotImplementedError('Abstract method. Implement in subclass')

    def get_item(self):
        """
        Return a reference to the PTGraphicsItem associated with this RangeFeature.
        :return: PTGraphicsItem
        """
        return self._graphics_item

    def set_item(self, item):
        """
        Store a reference to the PTGraphicsItem associated with this RangeFeature.
        :param item: PTGraphicsItem (i.e. CameraItem, TargetItem etc.)
        :return:
        """
        self._graphics_item = item

    def get_widget(self):
        """
        Return a reference to the widget associated with this RangeFeature
        :return: CameraInfoWidget, TargetInfoWidget or None
        """
        return self._graphics_widget

    def set_widget(self, widget):
        """
        Store a reference to the CameraInfoWidget/TargetInfoWidget associated with this RangeFeature.
        TODO: Have InfoWidgets inherit from the same parent-info-widget-class.
        :param widget: CameraInfoWidget or TargetInfoWidget
        :return:
        """
        self._graphics_widget = widget
