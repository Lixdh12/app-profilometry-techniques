import sys
from PyQt5.QtWidgets import QFrame,QGroupBox, QLabel,QHBoxLayout, QLineEdit, QComboBox, QRadioButton, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure
from screeninfo import get_monitors
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from acquire_display import AcquireDisplay


class WVistap(QWidget):
    def __init__(self, qframe):
        super().__init__(qframe)
        
        #Configurar fuente de texto
    #Agregar funciones
        self.vp_()
        try:
            self.acquire_display = AcquireDisplay(self.l_vp, self.canvas, self.ax, 0)
            self.acquire_display.live_camera()
        except:
            print('No se puede inicializar la cámara')

    

    def vp_(self):
        '''Sección de Vista previa. El usuario podrá visualizar la camara un live'''
        #Agregar frame para la sección
        #fr = QFrame(self)
        #self.layout.addWidget(fr)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #Agregar Grupo
        g_vp = QGroupBox('Vista previa')
        g_vp.setFont(QtGui.QFont("MS Shell Dlg 2", 11))
        self.layout.addWidget(g_vp)
        #Agregar layout
        self.l_vp = QVBoxLayout()
        g_vp.setLayout(self.l_vp)

        #Crear figura para agregar el canvas
        self.figure = Figure(figsize=(7, 4.5),  dpi=100)
        self.ax = self.figure.add_subplot()
        self.ax.set_yticks([])
        self.ax.set_xticks([])
         
        #Crear canvas para dibujar la imagen de la camara
        self.canvas = FigureCanvas(self.figure)
        self.l_vp.addWidget(self.canvas)