import sys
from PyQt5.QtWidgets import QFrame,QGroupBox, QLabel,QHBoxLayout, QLineEdit, QComboBox, QRadioButton, QPushButton, QVBoxLayout, QWidget
from screeninfo import get_monitors
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class WFringes(QWidget):
    #VARIABLES GLOBALES PARA USO DE TODAS LAS CLASES
    TEMPORAL = None
    
    def __init__(self, qframe):
        super().__init__(qframe)
        
        #Obtener los datos de los monitores conectados
        monitors = get_monitors()
        #Obtener datos del 1ro monitor
        self.monitor1 = monitors[0]
        try: 
          #Obtener datos del 2do monitor
          self.monitor2 = monitors[1]
        except:
             self.monitor2 = monitors[0]
             print('No hay monitores externos detectados')

          #Obtener las diensiones del monitor principal
        self.width = self.monitor1.width - 400 #WIDTH monitor 1
        self.height = self.monitor1.height - 300 #HEIGHT monitor 1

          
          

          #Configurar fuente de texto
        self.fon = QtGui.QFont("MS Shell Dlg 2", 10)

          
          #Agregar funciones
        self.fringes_()
        

    

    def fringes_(self):
        '''Sección de franjas. Se configura la intensidad media, modulación, frecuencia
          y resolución de las franjas para proyectarlas.'''
        #Agregar frame para la sección
        #fr = QFrame(self)
        #self.layout.addWidget(fr)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #Agregar Grupo
        g_fr = QGroupBox('Generación de franjas')
        g_fr.setFont(QtGui.QFont("MS Shell Dlg 2", 11))
        self.layout.addWidget(g_fr)
        #Agregar layout
        l_fr = QVBoxLayout()
        g_fr.setLayout(l_fr)
        #fr.setGeometry(0,0,0,0)

        '''Agregar etiquetas, cajas de texto, combobox, buttons'''
        #Etiqueta. Intensidad media - a
        lb1 = QLabel('Intensidad media:')
        lb1.setFont(self.fon)
        #Caja de texto
        self.e_a = QLineEdit()
        self.e_a.setFont(self.fon)
        self.e_a.setFixedSize(150, 30)
        self.e_a.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Justificar el texto
        self.e_a.setMaxLength(5)
        #Agregrar al layout
        gl_fr1 = QHBoxLayout()
        gl_fr1.addWidget(lb1)
        gl_fr1.addWidget(self.e_a)
        #Agregar al grupo
        l_fr.addLayout(gl_fr1)
        
        #Etiqueta. Intensidad de modulación - b
        lb2 = QLabel('Modulación:')
        lb2.setFont(self.fon)
        #Caja de texto
        self.e_b = QLineEdit()
        self.e_b.setFont(self.fon)
        self.e_b.setFixedSize(150, 30)
        self.e_b.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.e_b.setMaxLength(5)
        #Agregar al layout
        gl_fr2 = QHBoxLayout()
        gl_fr2.addWidget(lb2)
        gl_fr2.addWidget(self.e_b)
        #Agregar al grupo
        l_fr.addLayout(gl_fr2)

        #Etiqueta. Frecuencia o perído - w
        lb3 = QLabel('Frecuencia:')
        lb3.setFont(self.fon)
        #Caja de texto
        self.e_w = QLineEdit()
        self.e_w.setFont(self.fon)
        self.e_w.setFixedSize(150, 30)
        self.e_w.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.e_w.setMaxLength(5)
        #Agregar al layout
        gl_fr3 = QHBoxLayout()
        gl_fr3.addWidget(lb3)
        gl_fr3.addWidget(self.e_w)
        #Agregar al grupo
        l_fr.addLayout(gl_fr3)

        global TEMPORAL
        TEMPORAL = self.e_w

        #Etiqueta. Resolución - sx
        lb4 = QLabel('Resolución:')
        lb4.setFont(self.fon)
        #Comprobar si existe un 2do monitor
        self.combo = QComboBox()
        self.combo.setFont(self.fon)
        try:
             #variable por default
             self.resolution = [self.monitor2.width, self.monitor2.height]
             self.combo.addItems([
                  str(self.monitor2.width)+'x'+str(self.monitor2.height),
                    "1024x768",
                    "800x600"
                  ])
        except:
             self.resolution = [self.monitor1.width, self.monitor1.height]
             self.combo.addItems([
                  str(self.monitor1.width)+'x'+str(self.monitor1.height),
                    "1024x768",
                    "800x600"
                  ])
        #Agregar al layout
        gl_fr4 = QHBoxLayout()
        gl_fr4.addWidget(lb4)
        gl_fr4.addWidget(self.combo)
        #Agregar evento al combo
        self.combo.currentIndexChanged.connect(self.handle_combobox_change)
        #Agregar al grupo
        l_fr.addLayout(gl_fr4)

    def mostrar(self):
            self.a = self.e_a.text()
            self.b = self.e_b.text()
            print(self.a, self.a)
    
    def handle_combobox_change(self, index):
        selected_option = self.sender().currentText()
        print("Opción seleccionada:", selected_option)
        