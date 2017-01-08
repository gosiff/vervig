from model.features import HouseFeature
import copy

__author__ = 'Fredrik Salovius'


class Fuse(HouseFeature):
    def __init__(self, name):
        super(Fuse, self).__init__(name)

    def __getstate__(self):
        d = copy.copy(self.__dict__)
        del d['_graphics_item']
        del d['_graphics_widget']
        return d

    def __setstate__(self, state):
        """
        Define deserialization of object from the state-dict.
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

        self.__init__("")
        self.__dict__.update(state)

    def get_feature_type(self):
        return 'Fuse'
