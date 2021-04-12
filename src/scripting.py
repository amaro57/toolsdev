import pymel.core as pmc
from pymel.core.system import Path
import re
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    """Return the Maya main window widget"""
    main_window = omui.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):
    """Scatter Tool UI Class"""
    
    
    def __init__(self):
        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Smart Save")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        """self.scenefile = SceneFile()"""
        self.create_ui()
        """self.create_connections()"""
        
    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 30px")
        self.scatter_lay = self._create_scatter_ui()
        self.scale_lay = self._create_scale_ui()
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.source_lay)
        self.main_lay.addLayout(self.filename_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)
        
    def create_connections(self):
        """Connect Signals and Slots"""
        
    def _create_scatter_ui(self):
        layout = self._create_scale_headers()
        self.source_txt = QtWidgets.QTextEdit()
        self.source_txt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.source_btn = QtWidgets.QPushButton("Scatter Source")
        self.dest_txt = QtWidgets.QTextEdit()
        self.dest_txt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.dest_btn = QtWidgets.QPushButton("Scatter Destination")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.source_txt)
        layout.addWidget(self.source_btn)
        layout.addWidget(self.dest_txt)
        layout.addWidget(self.dest_btn)
        return layout
    
    def _create_scale_ui(self):
        layout = self._create_scale_headers()
        
    def _create_scale_headers(self):
		self.scale_title_lbl = QtWidgets.QLabel("Random Scale")
        self.title_lbl.setStyleSheet("font: bold 30px")
        self.scalex_header_lbl = QtWidgets.QLabel("X")
        self.scalex_header_lbl.setStyleSheet("font: bold")
        self.scaley_header_lbl = QtWidgets.QLabel("Y")
        self.scaley_header_lbl.setStyleSheet("font: bold")
        self.scalez_header_lbl = QtWidgets.QLabel("Z")
        self.scalez_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scale_title_lbl, 0, 0)
        layout.addWidget(self.scalex_header_lbl, 1, 0)
        layout.addWidget(self.scaley_header_lbl, 1, 3)
        layout.addWidget(self.scalez_header_lbl, 1, 6)
        return layout
        
    
    
