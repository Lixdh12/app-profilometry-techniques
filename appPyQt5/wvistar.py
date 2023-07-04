import os
from PyQt5.QtWidgets import QFrame,QGroupBox, QLabel,QHBoxLayout, QLineEdit, QComboBox, QRadioButton, QPushButton, QVBoxLayout, QWidget
from mayavi.mlab import contour3d
from numpy import cos
os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi import mlab
#from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from pyface.qt import QtGui, QtCore
import numpy as np

 ## create Mayavi Widget and show

class Visualization(HasTraits):
        scene = Instance(MlabSceneModel, ())

        @on_trait_change('scene.activated')
        def update_plot(self):
        ## PLot to Show 
            pixeles = 100 #(pixeles, pixeles)

            x = np.linspace(-1,1,pixeles,  endpoint=True)
            y = np.linspace(-1,1,pixeles,  endpoint=True)

            x_, y_ = np.meshgrid(x, y)
            x0 = np.mean(x_)
            y0 = np.mean(y_)
            ## función g
            g =  0.2 * np.exp(- ((x_ - x0)**2 +  (y_ - y0)**2) / (2 * np.var(x_)))  
            mlab.mesh(x_, y_, g)
            """ x, y, z = np.ogrid[-3:3:60j, -3:3:60j, -3:3:60j]
            t = 0
            Pf = 0.45+((x*cos(t))*(x*cos(t)) + (y*cos(t))*(y*cos(t))-(z*cos(t))*(z*cos(t)))
            obj = contour3d(Pf, contours=[0], transparent=False) """

        view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                         height=400, width=720, show_label=False),
                    resizable=True )


class WVistar(QWidget):
    def __init__(self, qframe):
        super().__init__(qframe)
        
        #Configurar fuente de texto
    #Agregar funciones
        self.vr_()

    

    def vr_(self):
        '''Sección de Vista de reconstrucción. El usuario podrá visualizar el objeto 3D'''
        #Agregar frame para la sección
        #fr = QFrame(self)
        #self.layout.addWidget(fr)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #Agregar Grupo
        g_vr = QGroupBox('Vista de reconstrucción')
        g_vr.setFont(QtGui.QFont("MS Shell Dlg 2", 11))
        self.layout.addWidget(g_vr)
        #Agregar layout
        l_vr = QVBoxLayout()
        l_vr.setContentsMargins(0,0,0,0)
        l_vr.setSpacing(0)
        g_vr.setLayout(l_vr)
        
        self.visualization = Visualization()
        self.ui = self.visualization.edit_traits(parent=g_vr,
                                                     kind='subpanel').control
        l_vr.addWidget(self.ui)
        self.ui.setParent(g_vr)

        
   
