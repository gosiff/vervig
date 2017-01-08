import pickle
import sip


sip.setapi('QString', 2)

__author__ = 'Fredrik Salovius'
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from model.house_model import HouseModel
from StringUtils import resource_path
import os
import sys
from view.main_view import MainviewWidget


class Electrical_Scheme(QtGui.QMainWindow):

    def __init__(self):
        super(Electrical_Scheme, self).__init__()
        uic.loadUi(resource_path(os.path.join('ui', 'main.ui')), self)

        self.dialog_path = ""
        self.filename = None
        new_project = self.findChild(QtGui.QAction, "actionNew_Project")
        new_project.triggered.connect(self.newProject)
        save_project = self.findChild(QtGui.QAction, "actionSave_Project")
        save_project.triggered.connect(self.saveProject)
        save_project.setEnabled(False)
        save_project_as = self.findChild(QtGui.QAction, "actionSave_Project_As")
        save_project_as.triggered.connect(self.saveProjectAs)
        save_project_as.setEnabled(False)

        load_project = self.findChild(QtGui.QAction, "actionOpen_Project")
        load_project.triggered.connect(self.openProject)



    def newProject(self):
        print 'new project'
        self.filename = QtGui.QFileDialog.getSaveFileName(parent=None, caption="New Project file",
                                              directory=self.dialog_path,
                                              filter="Project files (*.cproj)")
        if not self.filename:
            return
        self.dialog_path = os.path.dirname(self.filename)
        self.setup_project()


        save_project = self.findChild(QtGui.QAction, "actionSave_Project")
        save_project_as = self.findChild(QtGui.QAction, "actionSave_Project_As")
        save_project.setEnabled(True)
        save_project_as.setEnabled(True)


    def saveProject(self):
        print 'save project'
        model = self.main_view.model
        model.update_save_time()
        if self.filename is None:
            self.filename = QtGui.QFileDialog.getSaveFileName(parent=None, caption="Save project",
                                                  directory=self.dialog_path,
                                                  filter="Project files (*.cproj)")
            if not self.filename:
                return
            self.dialog_path = os.path.dirname(self.filename)
        try:
            # save to tmp file first, so we don't corrupt the original file
            with open(self.filename + "tmp", 'wb') as file_:
                pickle.dump(model, file_, protocol=2)

            # then we replace old file with new file
            if os.path.exists(self.filename):
                os.remove(self.filename)
            os.rename(self.filename + "tmp", self.filename)

            # self.main_view.model.get_invoker().set_save_point()

            # range_model.save_project(self.filename)
            print "Project Saved!"
        except Exception as ex:
            msg = QtGui.QMessageBox()
            msg.setText("Error saving project (" + ex.__class__.__name__ + ": " + ex.message + ")")
            msg.exec_()

    def saveProjectAs(self):
        old_filename = self.filename
        self.filename = QtGui.QFileDialog.getSaveFileName(parent=None, caption="Save project as",
                                                          directory=self.dialog_path,
                                                          filter="Project files (*.cproj)")
        if not self.filename:
            self.filename = old_filename
            return

        self.dialog_path = os.path.dirname(self.filename)
        self.saveProject()

    def openProject(self):

        self.filename = QtGui.QFileDialog.getOpenFileName(parent=None, caption="Open project",
                                          directory=self.dialog_path,
                                          filter="Project files (*.cproj)")
        if not self.filename:
            return

        self.dialog_path = os.path.dirname(self.filename)

        with open(self.filename, 'rb') as file_:
            new_range_model = pickle.load(file_)

        # Electrical_Scheme.update_range_model(new_range_model)

        self.setup_project(new_range_model)
        save_project = self.findChild(QtGui.QAction, "actionSave_Project")
        save_project_as = self.findChild(QtGui.QAction, "actionSave_Project_As")
        save_project.setEnabled(True)
        save_project_as.setEnabled(True)
        print "Project Opened!"
        print 'open project'

    def setup_project(self, model=None):
        if model is None:
            model = HouseModel()

        model.project_path = self.dialog_path
        self.main_view = MainviewWidget(model, self)
        self.setCentralWidget(self.main_view)



app = QtGui.QApplication(sys.argv)
form = Electrical_Scheme()
form.show()
sys.exit(app.exec_())
