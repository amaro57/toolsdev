import logging

import pymel.core as pmc
from pymel.core.system import Path
import re
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the Maya main window widget"""
    main_window = omui.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):
    """Smart Class UI Class"""
    
    def __init__(self):
        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Smart Save")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.scenefile = SceneFile()
        self.create_ui()
        
    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.folder_lay = self._create_folder_ui()
        self.filename_lay = self._create_filename_ui()
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.folder_lay)
        self.main_lay.addLayout(self.filename_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)
        
    def _create_button_ui(self):
        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_increment_btn = QtWidgets.QPushButton("Save Increment")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.save_btn)
        layout.addWidget(self.save_increment_btn)
        return layout
        
    def _create_filename_ui(self):
        layout = self._create_filename_headers()
        self.descriptor_le = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.descriptor_le.setMinimumWidth(100)
        self.task_le = QtWidgets.QLineEdit(self.scenefile.task)
        self.task_le.setFixedWidth(50)
        self.ver_sbx = QtWidgets.QSpinBox()
        self.ver_sbx.setValue(self.scenefile.ver)
        self.ver_sbx.setFixedWidth(50)
        self.ver_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ext_lbl = QtWidgets.QLabel(".ma")
        layout.addWidget(self.descriptor_le, 1, 0)
        layout.addWidget(QtWidgets.QLabel("_"), 1, 1)
        layout.addWidget(self.task_le, 1, 2)
        layout.addWidget(QtWidgets.QLabel("_v"), 1, 3)
        layout.addWidget(self.ver_sbx, 1, 4)
        layout.addWidget(self.ext_lbl, 1, 5)
        return layout
    
    def _create_filename_headers(self):
        self.descriptor_header_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_header_lbl.setStyleSheet("font: bold")
        self.task_header_lbl = QtWidgets.QLabel("Task")
        self.task_header_lbl.setStyleSheet("font: bold")
        self.ver_header_lbl = QtWidgets.QLabel("Version")
        self.ver_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.descriptor_header_lbl, 0, 0)
        layout.addWidget(self.task_header_lbl, 0, 2)
        layout.addWidget(self.ver_header_lbl, 0, 4)
        return layout
        
    def _create_folder_ui(self):
        default_folder = Path(cmds.workspace(rootDirectory=True, query=True))
        default_folder = default_folder / "scenes"
        self.folder_le = QtWidgets.QLineEdit(default_folder)
        self.folder_browse_btn = QtWidgets.QPushButton("...")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.folder_le)
        layout.addWidget(self.folder_browse_btn)
        return layout

class SceneFile(object):

    def __init__(self, path=None):
        self.folder_path = Path(cmds.workspace(query=True, rootDirectory=True)) / "scenes"
        self.descriptor = 'main'
        self.task = 'model'
        self.ver = 1
        self.ext = '.ma'
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.info("Intialize with default properties")
            return
        self._init_from_path(path)

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task, ver=self.ver, ext=self.ext)

    @property
    def path(self):
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = re.findall(
            '([^_]+)+', path.name.stripext())
        self.ver = int(ver.split("v")[-1])

    def save(self):
        """Saves the scene file.

        Returns:
            Path: The path to the scene file if successful
        """
        try:
            return pmc.system.saveAs(self.path)
        except:
            log.warning(
                "Missing directory in specified path. Creating directory")
            self.folder_path.mkdir_p()
            return pmc.system.saveAs(self.path)

    def next_avail_ver(self):
        """Returns the next available version number in a folder."""
        # pattern = f"{descriptor}_{task}_v*{ext}"  R.I.P. Maya Python still on Python 2
        pattern = "{descriptor}_{task}_v*{ext}".format(
            descriptor=self.descriptor, task=self.task, ext=self.ext)
        matching_scenefiles = []
        for file_ in self.folder_path.files():
            if file_.name.fnmatch(pattern):
                matching_scenefiles.append(file_)
        if not matching_scenefiles:
            return 1
        matching_scenefiles.sort(reverse=True)
        latest_scenefile = matching_scenefiles[0]
        # How do I get auto complete here? Does it not work because latest_scene is dynamic?
        latest_scenefile = latest_scenefile.name.stripext()
        latest_ver_num = int(latest_scenefile.split("_v")[-1])
        return latest_ver_num + 1

    def increment_save(self):
        """Increments the version and saves the scene

        If the exisiting version of a file already exists, it should increment
        from the largest version number available in the folder.

        Returns:
            Path: The path to the scene file if successful
        """
        self.ver = self.next_avail_ver()
        self.save()


# I get Error: WindowsError: file C:\Program Files\Autodesk\Maya2020\Python\lib\site-packages\pymel\util\path.py line 483: 3 
# when in a new scene. Why?