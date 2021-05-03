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
        self.rndseed_lay = self._create_random_seed_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.scatter_lay)
        self.main_lay.addLayout(self.scatter_btn_lay)
        self.main_lay.addLayout(self.scale_lay)
        self.main_lay.addLayout(self.rotate_lay)
        self.main_lay.addLayout(self.rndseed_lay)
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
        seed = self.rndseed_seed_sbx.value()
        percent_scatter = self.perct_sbx.value()
        percent_scatter = float(percent_scatter) / 100  #no need to strip the %, its a suffix added by Qt
        align_normal = self.align_cbx.isChecked()
        relative_offset = self.offset_cbx.isChecked()
        scale_val = [self.scalex_min_sbx.value(), self.scalex_max_sbx.value(),
                          self.scaley_min_sbx.value(), self.scaley_max_sbx.value(),
                          self.scalez_min_sbx.value(), self.scalez_max_sbx.value()]
        rotate_val = [self.rotatex_min_sbx.value(), self.rotatex_max_sbx.value(),
                           self.rotatey_min_sbx.value(), self.rotatey_max_sbx.value(),
                           self.rotatez_min_sbx.value(), self.rotatez_max_sbx.value()]
        offset_val = [self.offset_min_sbx.value(), self.offset_max_sbx.value()]
        self.scenefile.scatter(seed, percent_scatter, align_normal, scale_val, rotate_val, offset_val, relative_offset)

    def _create_scatter_ui(self):
        self.source_txt = QtWidgets.QTextEdit()
        self.source_txt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.source_txt.setFixedHeight(30)
        self.source_btn = QtWidgets.QPushButton("Set Scatter Source")
        self.dest_txt = QtWidgets.QTextEdit()
        self.dest_txt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.dest_txt.setFixedHeight(50)
        self.dest_btn = QtWidgets.QPushButton("Set Scatter Destination")
        layout = self._create_scatter_controls()
        layout.addWidget(self.source_btn, 0, 0)
        layout.addWidget(self.source_txt, 0, 1)
        layout.addWidget(self.dest_btn, 0, 2)
        layout.addWidget(self.dest_txt, 0, 3)
        return layout    
        #Improvement: Refactor this to better nest/group widgets, better alignment and positioning controls
        #This nested and return layout structure feels too rabbit-holey/uneasy to read, find better soultion?
    
    def _create_scatter_controls(self):
        self.perct_sbx_lbl = QtWidgets.QLabel("Percentage Scatter")
        self.perct_sbx_lbl.setStyleSheet("font: bold")
        self.perct_sbx = QtWidgets.QDoubleSpinBox()
        self.perct_sbx.setDecimals(1)
        self.perct_sbx.setValue(100)
        self.perct_sbx.setSuffix(" %")
        self.align_cbx_lbl = QtWidgets.QLabel("Align with normals?")
        self.align_cbx_lbl.setStyleSheet("font: bold")
        self.align_cbx = QtWidgets.QCheckBox()
        self.offset_min_sbx_lbl = QtWidgets.QLabel("Random Offset Min")
        self.offset_min_sbx_lbl.setStyleSheet("font: bold")
        self.offset_min_sbx = QtWidgets.QDoubleSpinBox()
        self.offset_min_sbx.setDecimals(2)
        self.offset_min_sbx.setSingleStep(0.1)
        self.offset_min_sbx.setMinimum(-99)
        self.offset_max_sbx_lbl = QtWidgets.QLabel("Random Offset Max")
        self.offset_max_sbx_lbl.setStyleSheet("font: bold")
        self.offset_max_sbx = QtWidgets.QDoubleSpinBox()
        self.offset_max_sbx.setDecimals(2)
        self.offset_max_sbx.setSingleStep(0.1)
        self.offset_max_sbx.setMinimum(-99)
        self.offset_cbx_lbl = QtWidgets.QLabel("Object relative offset?")
        self.offset_cbx_lbl.setStyleSheet("font: bold")
        self.offset_cbx = QtWidgets.QCheckBox()
        layout = QtWidgets.QGridLayout()
        perct_sbx = QtWidgets.QHBoxLayout()
        offset_sbx = QtWidgets.QHBoxLayout()
        offset_cbx = QtWidgets.QHBoxLayout()
        perct_sbx.addWidget(self.perct_sbx_lbl)
        perct_sbx.addWidget(self.perct_sbx)
        align_cbx = QtWidgets.QHBoxLayout()
        align_cbx.addWidget(self.align_cbx_lbl)
        align_cbx.addWidget(self.align_cbx)
        offset_sbx.addWidget(self.offset_min_sbx_lbl)
        offset_sbx.addWidget(self.offset_min_sbx)
        offset_sbx.addWidget(self.offset_max_sbx_lbl)
        offset_sbx.addWidget(self.offset_max_sbx)
        offset_cbx.addWidget(self.offset_cbx_lbl)
        offset_cbx.addWidget(self.offset_cbx)
        layout.addLayout(perct_sbx, 1, 0, alignment=QtCore.Qt.AlignCenter)
        layout.addLayout(align_cbx, 1, 1,  alignment=QtCore.Qt.AlignCenter)
        layout.addLayout(offset_sbx, 1, 2, alignment=QtCore.Qt.AlignCenter)
        layout.addLayout(offset_cbx, 1, 3, alignment=QtCore.Qt.AlignCenter)
        return layout

    def _create_scale_ui(self):
        layout = self._create_scale_headers()
        self.scalex_min_sbx = QtWidgets.QDoubleSpinBox()
        self.scalex_min_sbx.setDecimals(1)
        self.scalex_min_sbx.setSingleStep(0.1)
        self.scalex_min_sbx.setValue(1)
        self.scaley_min_sbx = QtWidgets.QDoubleSpinBox()
        self.scaley_min_sbx.setDecimals(1)
        self.scaley_min_sbx.setSingleStep(0.1)
        self.scaley_min_sbx.setValue(1)
        self.scalez_min_sbx = QtWidgets.QDoubleSpinBox()
        self.scalez_min_sbx.setDecimals(1)
        self.scalez_min_sbx.setSingleStep(0.1)
        self.scalez_min_sbx.setValue(1)
        self.scalex_max_sbx = QtWidgets.QDoubleSpinBox()
        self.scalex_max_sbx.setDecimals(1)
        self.scalex_max_sbx.setSingleStep(0.1)
        self.scalex_max_sbx.setValue(1)
        self.scaley_max_sbx = QtWidgets.QDoubleSpinBox()
        self.scaley_max_sbx.setDecimals(1)
        self.scaley_max_sbx.setSingleStep(0.1)
        self.scaley_max_sbx.setValue(1)
        self.scalez_max_sbx = QtWidgets.QDoubleSpinBox()
        self.scalez_max_sbx.setDecimals(1)
        self.scalez_max_sbx.setSingleStep(0.1)
        self.scalez_max_sbx.setValue(1) #Cleaner way to organize all these set methods?
        layout.addWidget(self.scalex_min_sbx, 2, 0)
        layout.addWidget(self.scalex_max_sbx, 2, 1)
        layout.addWidget(self.scaley_min_sbx, 2, 2)
        layout.addWidget(self.scaley_max_sbx, 2, 3)
        layout.addWidget(self.scalez_min_sbx, 2, 4)
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
        layout.addWidget(self.scalex_max_header_lbl, 1, 1)
        layout.addWidget(self.scaley_min_header_lbl, 1, 2)
        layout.addWidget(self.scaley_max_header_lbl, 1, 3)
        layout.addWidget(self.scalez_min_header_lbl, 1, 4)
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
        layout.addWidget(self.rotatex_max_sbx, 2, 1)
        layout.addWidget(self.rotatey_min_sbx, 2, 2)
        layout.addWidget(self.rotatey_max_sbx, 2, 3)
        layout.addWidget(self.rotatez_min_sbx, 2, 4)
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
        layout.addWidget(self.rotatex_max_header_lbl, 1, 1)
        layout.addWidget(self.rotatey_min_header_lbl, 1, 2)
        layout.addWidget(self.rotatey_max_header_lbl, 1, 3)
        layout.addWidget(self.rotatez_min_header_lbl, 1, 4)
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
    
    def _create_random_seed_ui(self):
        self.rndseed_title_lbl = QtWidgets.QLabel("Random Seed")
        self.rndseed_title_lbl.setStyleSheet("font: bold 20px")
        self.rndseed_seed_sbx = QtWidgets.QSpinBox()
        self.rndseed_seed_sbx.setRange(0, 99999)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.rndseed_title_lbl)
        layout.addWidget(self.rndseed_seed_sbx)
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
            
        

    def scatter(self, seed, percent, align, scale, rotate, offset, relativeOffset):
        random.seed(seed)
        random_amount = int(round(len(self.destSel) * percent))
        percentage_select = random.sample(self.destSel, k=random_amount) #Refactor to use a flag instead of always running?
        if cmds.objectType(self.sourceObject, isType="transform"):
            for vertex in percentage_select:
                scaleX = random.uniform(scale[0], scale[1])
                scaleY = random.uniform(scale[2], scale[3])
                scaleZ = random.uniform(scale[4], scale[5])
                rotateX = random.uniform(rotate[0], rotate[1])
                rotateY = random.uniform(rotate[2], rotate[3])
                rotateZ = random.uniform(rotate[4], rotate[5])
                offsetY = random.uniform(offset[0], offset[1])
                print(offsetY)
                scatter_instance = cmds.instance(self.sourceObject)
                position = cmds.pointPosition(vertex, w=True)
                meshvert = pmc.MeshVertex(vertex)
                vtx_normal = meshvert.getNormal()
                up_vector = pmc.datatypes.Vector(0.0, 1.0, 0)
                tangent = vtx_normal.cross(up_vector).normal()
                tangent2 = vtx_normal.cross(tangent).normal()
                matrix_transform = [tangent2.x, tangent2.y, tangent2.z, 0.0,
                                    vtx_normal.x, vtx_normal.y, vtx_normal.z, 0.0,
                                    tangent.x, tangent.y, tangent.z, 0.0,
                                    position[0], position[1], position[2], 1.0]
                if align:
                    cmds.xform(scatter_instance, ws=True, m=matrix_transform) #How to include scale and rotation into 4x4 matrix supplied?
                    cmds.scale(scaleX, scaleY, scaleZ, scatter_instance)
                    if relativeOffset:  #Better way to do this than two flags? Dislike how this feels
                        cmds.move(0, offsetY, 0, scatter_instance, r=True, os=True, wd=True)
                    else:
                        cmds.move(0, offsetY, 0, scatter_instance, r=True, ws=True)
                    #cmds.rotate(rotateX, rotateY, rotateZ, scatter_instance)
                    #This method is not constraining instances to parent vertices. What's missing vs things like Point on Poly?
                    continue
                cmds.xform(scatter_instance, scale=[scaleX, scaleY, scaleZ], rotation=[rotateX, rotateY, rotateZ],
                        translation=[position[0], position[1], position[2]], ws=True)
                if relativeOffset:
                    cmds.move(0, offsetY, 0, scatter_instance, r=True, os=True, wd=True)
                else:
                    cmds.move(0, offsetY, 0, scatter_instance, r=True, ws=True)