import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame,QHBoxLayout, QGridLayout
from screeninfo import get_monitors
from PyQt5.QtCore import Qt

from wfringes import WFringes
from wunwarp import WUnwarp
from wvistap import WVistap
from wvistar import WVistar

class Main():
    def __init__(self):
        # Creación de la aplicación y la ventana principal
        app = QApplication(sys.argv)
        window = QMainWindow()

        window.setWindowTitle("Perfilometría por Proyección de Franjas") #Title of window

        #Obtener los datos de los monitores conectados
        monitors = get_monitors()
        #Obtener las diensiones del monitor principal
        WIDTH = monitors[0].width - 400
        HEIGHT = monitors[0].height - 300
        #Calcular las coordenadas (x,y) de la pantalla
        x = (monitors[0].width - WIDTH) // 2
        y = (monitors[0].height - HEIGHT) // 2
        # Dar ubicación a la ventana
        window.setGeometry(x, y, WIDTH, HEIGHT)
        window.setFixedSize(WIDTH, HEIGHT)

         # Llamada a la función para inicializar el contenido de la ventana
        self.inicializar_(window, WIDTH, HEIGHT)

        # Mostrar la ventana principal y ejecutar la aplicación
        window.show()
        sys.exit(app.exec_())

    def inicializar_(self, w, WIDTH, HEIGHT):
        # Crear widget central
        central_widget = QWidget(w)
        w.setCentralWidget(central_widget)

         # Crear layout principal para el widget central
        layout = QGridLayout(central_widget)
        

        # Crear frame fringes 
        frame_fringes = QFrame()
        frame_fringes .setFrameStyle(QFrame.Panel | QFrame.Raised)
        frame_fringes .setLineWidth(1)
        layout.addWidget(frame_fringes, 0,0,1,1)

        # Crear frame unwap 
        frame_unw = QFrame()
        frame_unw .setFrameStyle(QFrame.Panel | QFrame.Raised)
        frame_unw  .setLineWidth(1)
        layout.addWidget(frame_unw,0, 1,1,1)

         # Crear frame unwap 
        #frame_i = QFrame()
        #frame_i .setFrameStyle(QFrame.Panel | QFrame.Raised)
        #frame_i  .setLineWidth(1)
        #layout.addWidget(frame_i,0, 2,1,1,)

        # Crear frame vista
        frame_vist = QFrame()
        frame_vist .setFrameStyle(QFrame.Panel | QFrame.Raised)
        frame_vist  .setLineWidth(1)
        layout.addWidget(frame_vist,1, 0,2,2)
        
        # Crear frame vista de reconstrucción
        frame_reco = QFrame()
        frame_reco .setFrameStyle(QFrame.Panel | QFrame.Raised)
        frame_reco  .setLineWidth(1)
        layout.addWidget(frame_reco,0, 3, 2,2)
        

        # Crear layout para el frame principal
        #frame_layout = QVBoxLayout(frame_principal)

        # Agregar widget personalizado al frame principal
        WFringes(frame_fringes)
        WUnwarp(frame_unw)
        WVistap(frame_vist)
        WVistar(frame_reco)

if __name__ == "__main__":
    Main()
    
