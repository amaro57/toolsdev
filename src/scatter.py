import pymel.core as pmc
from pymel.core.system import Path
import re
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import random


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
        self.main_lay.addLayout(self.rotate_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        """Connect Signals and Slots"""
        self.source_btn.clicked.connect(self._set_scatter_source)
        self.dest_btn.clicked.connect(self._set_scatter_dest)
        self.scatter_btn.clicked.connect(self._scatter)

    @QtCore.Slot()
    def _set_scatter_source(self):
        selection = self.scenefile.set_scatter_source()
        self.source_txt.setText(selection)

    @QtCore.Slot()
    def _set_scatter_dest(self):
        selection = self.scenefile.set_scatter_dest()
        self.dest_txt.setText(str(self.parseArray(selection)))

    @QtCore.Slot()
    def _scatter(self):
        percent_scatter = self.perct_sbx.value()
        align_normal = self.align_cbx.isChecked()
        scale_val = [self.scalex_min_sbx.value(), self.scalex_max_sbx.value(),
                          self.scaley_min_sbx.value(), self.scaley_max_sbx.value(),
                          self.scalez_min_sbx.value(), self.scalez_max_sbx.value()]
        rotate_val = [self.rotatex_min_sbx.value(), self.rotatex_max_sbx.value(),
                           self.rotatey_min_sbx.value(), self.rotatey_max_sbx.value(),
                           self.rotatez_min_sbx.value(), self.rotatez_max_sbx.value()]
        self.scenefile.scatter(percent_scatter, align_normal, scale_val, rotate_val)

    def _create_scatter_ui(self):
        self.source_txt = QtWidgets.QTextEdit()
        self.source_txt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.source_txt.setFixedHeight(30)
        self.source_btn = QtWidgets.QPushButton("Set Scatter Source")
        self.dest_txt = QtWidgets.QTextEdit()
        self.dest_txt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.dest_txt.setFixedHeight(50)
        self.dest_btn = QtWidgets.QPushButton("Set Scatter Destination")
        self.perct_sbx = QtWidgets.QDoubleSpinBox()
        self.perct_sbx.setDecimals(0)
        self.perct_sbx.setSuffix(" %")
        self.align_cbx = QtWidgets.QCheckBox()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.source_btn, 0, 0)
        layout.addWidget(self.source_txt, 0, 1)
        layout.addWidget(self.dest_btn, 0, 2)
        layout.addWidget(self.dest_txt, 0, 3)
        layout.addWidget(self.perct_sbx, 1, 1)
        layout.addWidget(self.align_cbx, 1, 3)
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
        layout.addWidget(self.scaley_min_sbx, 2, 1)
        layout.addWidget(self.scalez_min_sbx, 2, 2)
        layout.addWidget(self.scalex_max_sbx, 2, 3)
        layout.addWidget(self.scaley_max_sbx, 2, 4)
        layout.addWidget(self.scalez_max_sbx, 2, 5)
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
        layout.addWidget(self.scaley_min_header_lbl, 1, 1)
        layout.addWidget(self.scalez_min_header_lbl, 1, 2)
        layout.addWidget(self.scalex_max_header_lbl, 1, 3)
        layout.addWidget(self.scaley_max_header_lbl, 1, 4)
        layout.addWidget(self.scalez_max_header_lbl, 1, 5)
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
        layout.addWidget(self.rotatey_min_sbx, 2, 1)
        layout.addWidget(self.rotatez_min_sbx, 2, 2)
        layout.addWidget(self.rotatex_max_sbx, 2, 3)
        layout.addWidget(self.rotatey_max_sbx, 2, 4)
        layout.addWidget(self.rotatez_max_sbx, 2, 5)
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
        layout.addWidget(self.rotatey_min_header_lbl, 1, 1)
        layout.addWidget(self.rotatez_min_header_lbl, 1, 2)
        layout.addWidget(self.rotatex_max_header_lbl, 1, 3)
        layout.addWidget(self.rotatey_max_header_lbl, 1, 4)
        layout.addWidget(self.rotatez_max_header_lbl, 1, 5)
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

    """Scenfile Operations"""

    def set_scatter_source(self):
        selection = cmds.ls(os=True, fl=True)
        self.sourceObject = selection[0]
        return self.sourceObject

    def set_scatter_dest(self):
        selection = cmds.ls(os=True, fl=True)
        self.destSel = cmds.filterExpand(
            selection, selectionMask=31, expand=True)
        if self.destSel is not None:
            print(self.destSel)
            return self.destSel
        else:
            convVert = cmds.polyListComponentConversion(selection, tv=True)
            self.destSel = cmds.filterExpand(
                convVert, selectionMask=31, expand=True)  
            print(self.destSel)
            return self.destSel
        """Is there a better way to do this than expanding selection.vtx[*] into every single vert?
            Only use and display selection.vtx[*], since a can only select one Warning is given"""
            
        

    def scatter(self, percent, align, scale, rotate):
        random.seed(1234)

        scaleX = random.uniform(scale[0], scale[1])
        scaleY = random.uniform(scale[2], scale[3])
        scaleZ = random.uniform(scale[4], scale[5])
        rotateX = random.uniform(rotate[0], rotate[1])
        rotateY = random.uniform(rotate[2], rotate[3])
        rotateZ = random.uniform(rotate[4], rotate[5])

        if cmds.objectType(self.sourceObject, isType="transform"):
            for vertex in self.destSel:
                newInstance = cmds.instance(self.sourceObject)
                position = cmds.pointPosition(vertex, w=True)
                cmds.move(
                    position[0],
                    position[1],
                    position[2],
                    newInstance,
                    a=True,
                    ws=True)
                cmds.scale(scaleX, scaleY, scaleZ, newInstance)
                cmds.rotate(rotateX, rotateY, rotateZ, newInstance)
