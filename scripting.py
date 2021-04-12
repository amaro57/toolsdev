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
        super(ScatterToolUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scenefile = SceneFile()
        self.create_ui()
        self.create_connections()
        
    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 30px")
        self.scatter_lay = self._create_scatter_ui()
        self.scatter_btn_lay = self._create_scatter_button_ui()
        self.scale_lay = self._create_scale_ui()
        self.scale_btn_lay = self._create_scale_button_ui()
        self.rotate_lay = self._create_rotate_ui()
        self.rotate_btn_lay = self._create_rotate_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.scatter_lay)
        self.main_lay.addLayout(self.scatter_btn_lay)
        self.main_lay.addLayout(self.scale_lay)
        self.main_lay.addLayout(self.scale_btn_lay)
        self.main_lay.addLayout(self.rotate_lay)
        self.main_lay.addLayout(self.rotate_btn_lay)
        self.setLayout(self.main_lay)
        
    def create_connections(self):
        """Connect Signals and Slots"""
        self.source_btn.clicked.connect(self._set_scatter_source)
        self.dest_btn.clicked.connect(self._set_scatter_dest)
        """self.scatter_btn.clicked.connect(self._scatter)
        self.scale_btn.clicked.connect(self._scale)
        self.rotate_btn.clicked.connect(self._rotate)"""
        
    @QtCore.Slot()
    def _set_scatter_source(self):
        selection = self.scenefile.set_scatter_source()
        self.source_txt.setText(selection[0])
    
    @QtCore.Slot()
    def _set_scatter_dest(self):
        selection = self.scenefile.set_scatter_dest()
        self.dest_txt.setText(str(self.parseArray(selection)))
        
    """@QtCore.Slot()
    def _scatter(self):
        
    @QtCore.Slot()
    def _scale(self):
        
    @QtCore.Slot()
    def _rotate(self):"""
        
    def _create_scatter_ui(self):
        layout = self._create_scale_headers()
        self.source_txt = QtWidgets.QTextEdit()
        self.source_txt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.source_txt.setFixedHeight(30)
        self.source_btn = QtWidgets.QPushButton("Set Scatter Source")
        self.dest_txt = QtWidgets.QTextEdit()
        self.dest_txt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.dest_txt.setFixedHeight(50)
        self.dest_btn = QtWidgets.QPushButton("Set Scatter Destination")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.source_txt)
        layout.addWidget(self.source_btn)
        layout.addWidget(self.dest_txt)
        layout.addWidget(self.dest_btn)
        return layout
    
    def _create_scale_ui(self):
        layout = self._create_scale_headers()
        self.scalex_min_sbx = QtWidgets.QDoubleSpinBox()
        self.scalex_min_sbx.setDecimals(1)
        self.scalex_min_sbx.setSingleStep(0.1)
        self.scaley_min_sbx = QtWidgets.QDoubleSpinBox()
        self.scaley_min_sbx.setDecimals(1)
        self.scaley_min_sbx.setSingleStep(0.1)
        self.scalez_min_sbx = QtWidgets.QDoubleSpinBox()
        self.scalez_min_sbx.setDecimals(1)
        self.scalez_min_sbx.setSingleStep(0.1)
        self.scalex_max_sbx = QtWidgets.QDoubleSpinBox()
        self.scalex_max_sbx.setDecimals(1)
        self.scalex_max_sbx.setSingleStep(0.1)
        self.scaley_max_sbx = QtWidgets.QDoubleSpinBox()
        self.scaley_max_sbx.setDecimals(1)
        self.scaley_max_sbx.setSingleStep(0.1)
        self.scalez_max_sbx = QtWidgets.QDoubleSpinBox()
        self.scalez_max_sbx.setDecimals(1)
        self.scalez_max_sbx.setSingleStep(0.1)
        layout.addWidget(self.scalex_min_sbx, 2, 0)
        layout.addWidget(self.scaley_min_sbx, 2, 3)
        layout.addWidget(self.scalez_min_sbx, 2, 6)
        layout.addWidget(self.scalex_max_sbx, 2, 1)
        layout.addWidget(self.scaley_max_sbx, 2, 4)
        layout.addWidget(self.scalez_max_sbx, 2, 7)
        return layout
        
    def _create_scale_headers(self):
        self.scale_title_lbl = QtWidgets.QLabel("Random Scale")
        self.scale_title_lbl.setStyleSheet("font: bold 20px")
        self.scalex_min_header_lbl = QtWidgets.QLabel("X Min")
        self.scalex_min_header_lbl.setStyleSheet("font: bold")
        self.scaley_min_header_lbl = QtWidgets.QLabel("Y Min")
        self.scaley_min_header_lbl.setStyleSheet("font: bold")
        self.scalez_min_header_lbl = QtWidgets.QLabel("Z Min")
        self.scalez_min_header_lbl.setStyleSheet("font: bold")
        self.scalex_max_header_lbl = QtWidgets.QLabel("X Max")
        self.scalex_max_header_lbl.setStyleSheet("font: bold")
        self.scaley_max_header_lbl = QtWidgets.QLabel("Y Max")
        self.scaley_max_header_lbl.setStyleSheet("font: bold")
        self.scalez_max_header_lbl = QtWidgets.QLabel("Z Max")
        self.scalez_max_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scale_title_lbl, 0, 0)
        layout.addWidget(self.scalex_min_header_lbl, 1, 0)
        layout.addWidget(self.scaley_min_header_lbl, 1, 3)
        layout.addWidget(self.scalez_min_header_lbl, 1, 6)
        layout.addWidget(self.scalex_max_header_lbl, 1, 1)
        layout.addWidget(self.scaley_max_header_lbl, 1, 4)
        layout.addWidget(self.scalez_max_header_lbl, 1, 7)
        return layout
    
    def _create_rotate_ui(self):
        layout = self._create_rotate_headers()
        self.rotatex_min_sbx = QtWidgets.QSpinBox()
        self.rotatex_min_sbx.setRange(0, 360)
        self.rotatey_min_sbx = QtWidgets.QSpinBox()
        self.rotatey_min_sbx.setRange(0, 360)
        self.rotatez_min_sbx = QtWidgets.QSpinBox()
        self.rotatez_min_sbx.setRange(0, 360)
        self.rotatex_max_sbx = QtWidgets.QSpinBox()
        self.rotatex_max_sbx.setRange(0, 360)
        self.rotatey_max_sbx = QtWidgets.QSpinBox()
        self.rotatey_max_sbx.setRange(0, 360)
        self.rotatez_max_sbx = QtWidgets.QSpinBox()
        self.rotatez_max_sbx.setRange(0, 360)
        self.rotatex_min_sbx.setWrapping(True)
        self.rotatey_min_sbx.setWrapping(True)
        self.rotatez_min_sbx.setWrapping(True)
        self.rotatex_max_sbx.setWrapping(True)
        self.rotatey_max_sbx.setWrapping(True)
        self.rotatez_max_sbx.setWrapping(True)
        layout.addWidget(self.rotatex_min_sbx, 2, 0)
        layout.addWidget(self.rotatey_min_sbx, 2, 3)
        layout.addWidget(self.rotatez_min_sbx, 2, 6)
        layout.addWidget(self.rotatex_max_sbx, 2, 1)
        layout.addWidget(self.rotatey_max_sbx, 2, 4)
        layout.addWidget(self.rotatez_max_sbx, 2, 7)
        return layout
    
    def _create_rotate_headers(self):
        self.rotate_title_lbl = QtWidgets.QLabel("Random Rotate")
        self.rotate_title_lbl.setStyleSheet("font: bold 20px")
        self.rotatex_min_header_lbl = QtWidgets.QLabel("X Min")
        self.rotatex_min_header_lbl.setStyleSheet("font: bold")
        self.rotatey_min_header_lbl = QtWidgets.QLabel("Y Min")
        self.rotatey_min_header_lbl.setStyleSheet("font: bold")
        self.rotatez_min_header_lbl = QtWidgets.QLabel("Z Min")
        self.rotatez_min_header_lbl.setStyleSheet("font: bold")
        self.rotatex_max_header_lbl = QtWidgets.QLabel("X Max")
        self.rotatex_max_header_lbl.setStyleSheet("font: bold")
        self.rotatey_max_header_lbl = QtWidgets.QLabel("Y Max")
        self.rotatey_max_header_lbl.setStyleSheet("font: bold")
        self.rotatez_max_header_lbl = QtWidgets.QLabel("Z Max")
        self.rotatez_max_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.rotate_title_lbl, 0, 0)
        layout.addWidget(self.rotatex_min_header_lbl, 1, 0)
        layout.addWidget(self.rotatey_min_header_lbl, 1, 3)
        layout.addWidget(self.rotatez_min_header_lbl, 1, 6)
        layout.addWidget(self.rotatex_max_header_lbl, 1, 1)
        layout.addWidget(self.rotatey_max_header_lbl, 1, 4)
        layout.addWidget(self.rotatez_max_header_lbl, 1, 7)
        return layout
    
    def _create_scatter_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout
    
    def _create_scale_button_ui(self):
        self.scale_btn = QtWidgets.QPushButton("Scale")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scale_btn)
        return layout
    
    def _create_rotate_button_ui(self):
        self.rotate_btn = QtWidgets.QPushButton("Rotate")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.rotate_btn)
        return layout
    
    def parseArray(self, selection):
        str1 = ", ".join(selection)
        return str1
    

class SceneFile(object):
    
    """def __init__(self):"""
        
    def set_scatter_source(self):
        self.sourceObject = cmds.ls(os=True, fl=True)
        return self.sourceObject[0]
        
    def set_scatter_dest(self):
        selection = cmds.ls(os=True, fl=True)
        self.destSel = cmds.filterExpand(selection, selectionMask=31, expand=True)
        print(self.destSel)
        return self.destSel
        
    """def scatter(self):
        
    def scale(self):
        
    def rotate(self):"""
