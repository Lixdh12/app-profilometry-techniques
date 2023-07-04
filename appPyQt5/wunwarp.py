import sys
from PyQt5.QtWidgets import QFrame,QGroupBox, QLabel,QHBoxLayout, QLineEdit, QComboBox, QRadioButton, QPushButton, QVBoxLayout, QWidget
from screeninfo import get_monitors
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from wfringes import WFringes

class WUnwarp(QWidget):
    def __init__(self, qframe):
        super().__init__(qframe)
        
        #Configurar fuente de texto
        self.fon = QtGui.QFont("MS Shell Dlg 2", 10)

    
    #Agregar funciones
        self.unwa_()

    

    def unwa_(self):
        '''Sección de desenvolvimiento. Selección de tipo de desenvolvimiento: espacial(x,y) y temporal.
        Y seleccionar el número de muestreos para el temporal'''
        #Agregar frame para la sección
        #fr = QFrame(self)
        #self.layout.addWidget(fr)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #Agregar Grupo
        g_un = QGroupBox('Desenvolvimiento')
        g_un.setFont(QtGui.QFont("MS Shell Dlg 2", 11))
        self.layout.addWidget(g_un)
        #Agregar layout
        l_un = QVBoxLayout()
        g_un.setLayout(l_un)

        '''Agregar etiquetas, cajas de texto, combobox, buttons'''
        #Etiqueta. Espacia / temporal
        lb1 = QLabel('Espacial/temporal:')
        lb1.setFont(self.fon)
        #Agregar combobox el tipo de tecnica a usar
        self.combo = QComboBox()
        self.combo.setFont(self.fon)
        self.combo.addItems([
                  "Espacial",
                    "Temporal"
                  ])
        
        #Agregar al layout
        gl_un1 = QHBoxLayout()
        gl_un1.addWidget(lb1)
        gl_un1.addWidget(self.combo)
        #Agregar evento al combo
        self.combo.currentIndexChanged.connect(self.handle_combobox_change)
        #Agregar al grupo
        l_un.addLayout(gl_un1)
        lb1.setFont(self.fon)

        gl_un2 = QHBoxLayout()
        #gl_un2.setEnabled(False)
        self.lb2 = QLabel('Muestreo:')
        self.lb2.setEnabled(False)
        self.lb2.setFont(self.fon)
        self.cb = QComboBox()
        self.cb.setEnabled(False)
        self.cb.setFont(self.fon)
        self.cb.addItems([
             'Lineal',
             'ELTS'
        ])
        #Agregar al layout
        gl_un2.addWidget(self.lb2)
        gl_un2.addWidget(self.cb)
        #Agregar evento al combo
        self.cb.currentIndexChanged.connect(self.handle_combobox_change_muestreo)
        #radio_button1.toggled.connect(self.handle_radio_button_toggle)
        l_un.addLayout(gl_un2)

        gl_un3 = QHBoxLayout()
        self.lb3 = QLabel('Número de muestreos:')
        self.lb3.setFont(self.fon)
        #Caja de texto
        self.e_n = QLineEdit()
        self.e_n.setEnabled(False)
        self.e_n.setFont(self.fon)
        self.e_n.setFixedSize(150, 30)
        self.e_n.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.e_n.setMaxLength(5)
        #Agregar al layout
        gl_un3.addWidget(self.lb3)
        gl_un3.addWidget(self.e_n)
        l_un.addLayout(gl_un3)

        #Agregar campo para el numero de pasos (ELTS)
        gl_un4 = QHBoxLayout()
        self.lb4 = QLabel('Número de pasos:')
        self.lb4.setFont(self.fon)
        #Caja de texto
        self.e_p = QLineEdit()
        self.e_p.setEnabled(False)
        self.e_p.setFont(self.fon)
        self.e_p.setFixedSize(150, 30)
        self.e_p.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.e_p.setMaxLength(5)
        #Agregar al layout
        gl_un4.addWidget(self.lb4)
        gl_un4.addWidget(self.e_p)
        l_un.addLayout(gl_un4)


    def mostrar(self):
            self.a = self.e_a.text()
            self.b = self.e_b.text()
            print(self.a, self.a)
    
    def handle_combobox_change(self, index):
        selected_option = self.sender().currentText()
        if selected_option == 'Espacial':
             
             self.lb2.setEnabled(False)#Campo de num de muestras
             self.cb.setEnabled(False) #Campo de seleccion (Lineal/ELTS)
             self.e_n.setEnabled(False) #Campo de num de muestras
             self.lb4.setEnabled(False) #Campo de num de pasos (ELTS)
             self.e_p.setEnabled(False)
             #WFringes.TEMPORAL.setEnabled(True)
        elif selected_option == 'Temporal':
             self.lb2.setEnabled(True)#Campo de num de muestras
             self.cb.setEnabled(True) #Campo de seleccion (Lineal/ELTS)
             self.e_n.setEnabled(True)#Campo de num de muestras
        print(selected_option)

             #WFringes.TEMPORAL.setEnabled(False)
    def handle_combobox_change_muestreo(self, index):
            selected_option = self.sender().currentText()
            if selected_option == 'Lineal':
                self.lb4.setEnabled(False)
                #self.lb4.setEnabled(False)
                self.e_p.setEnabled(False)
                #WFringes.TEMPORAL.setEnabled(True)
            
            elif selected_option == 'ELTS':
                self.lb4.setEnabled(True)
                #self.lb4.setEnabled(True)
                self.e_p.setEnabled(True)
            print(selected_option)
            