import copy

"""
Module containing classes for a Command Pattern. Every change of the model should be performed by issuing a
Command, with an execute and an undo method implemented. Every time a project is saved, a save point is set
at the LAST command. This lets us keep track of unsaved changes, which is when the last command does NOT
have a save point.
"""

__author__ = 'Joakim Hugmark'


class Invoker(object):
    """The INVOKER class"""
    def __init__(self):
        self._history = []
        self._undo_history = []

    def store_and_execute(self, command):
        command.execute()
        self._history.append(command)

    def undo_last(self):
        if len(self._history) > 0:
            cmd = self._history.pop()
            cmd.undo()
            self._undo_history.append(cmd)

    def redo_last(self):
        if len(self._undo_history) > 0:
            cmd = self._undo_history.pop()
            cmd.execute()
            self._history.append(cmd)

    def get_command_list_str(self):
        return "".join(cmd.get_description() + "\n" for cmd in self._history)

    def has_unsaved_changes(self):
        if len(self._history) > 0:
            return not self._history[-1].has_save_point()
        return False

    def set_save_point(self):
        for item in self._history:
            item.unset_save_point()
        if len(self._history) > 0:
            self._history[-1].set_save_point()


class Command(object):
    """The COMMAND interface"""
    def __init__(self, obj):
        self._obj = obj
        self._desc = "Generic Command"
        self._save = False

    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

    def get_description(self):
        return self._desc

    def set_save_point(self):
        self._save = True

    def unset_save_point(self):
        self._save = False

    def has_save_point(self):
        return self._save


class BatchCommand(Command):
    """Meta-command to execute a list of commands in one invocation"""
    def __init__(self, list_of_commands):
        super(BatchCommand, self).__init__(list_of_commands)
        self._desc = "Batch command:\n\t" + "\t".join(cmd.get_description() + "\n" for cmd in list_of_commands)

    def execute(self):
        for command in self._obj:
            command.execute()

    def undo(self):
        for command in reversed(self._obj):
            command.undo()


class GenericSetCommand(Command):
    """
    Command-"Template" that can be used for all actions that just uses a setter/getter.
    :param setter: A function-pointer to the setter-method for the object/property you want to change.
    :param getter: A function-pointer to the getter-method for the object/property you want to change.
    :param *args: The arguments you want to sent to the setter.
    NOTE: The setter and getter must be compatible to each other, meaning that setter(getter()) must be a
    valid operation that doesn't change the underlying model.
    """
    def __init__(self, setter, getter, *args):
        super(GenericSetCommand, self).__init__(None)
        self._args = args
        self._old_value = getter()
        self._setter = setter
        self._getter = getter
        self._desc = self._setter.im_class.__name__ + " " + self._setter.__name__ + " to " + str(*args)

    def execute(self):
        self._setter(*self._args)

    def undo(self):
        try:
            self._setter(*self._old_value)
        except TypeError:
            self._setter(self._old_value)


class AddFeatureCommand(Command):
    def __init__(self, add_method, set_method, all_features, feature):
        super(AddFeatureCommand, self).__init__(None)
        self._feature = feature
        self._add_method = add_method
        self._old_features = copy.copy(all_features)
        self._set_method = set_method
        self._desc = "Added " + feature.get_feature_type() + " " + feature.get_name()

    def execute(self):
        self._add_method(self._feature)

    def undo(self):
        self._set_method(self._old_features)


class DeleteFeatureCommand(Command):
    def __init__(self, delete_method, set_method, all_features, feature):
        super(DeleteFeatureCommand, self).__init__(None)
        self._feature = feature
        self._del_method = delete_method
        self._old_features = copy.copy(all_features)
        self._set_method = set_method
        self._desc = "Deleted " + feature.get_feature_type() + " " + feature.get_name()

    def execute(self):
        self._del_method(self._feature)

    def undo(self):
        self._set_method(self._old_features)