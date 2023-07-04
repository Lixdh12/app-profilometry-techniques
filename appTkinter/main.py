import tkinter as tk
from screeninfo import get_monitors
from window import Window
from tkinter import ttk
#from franges import Franges

class Main():
    def __init__(self):
        #creación de la ventana
        w = tk.Tk()
        w.title('Perfilometría por Proyección de Franjas')
        w.resizable(width=False, height=False)

        #Obtener los datos de los monitores conectados
        self.m = get_monitors()
        #Obtener las dimensiones del monitor principal
        WIDTH = (self.m[0].width-400)
        HEIGHT = (self.m[0].height-400)
        #Calcular las coordenadas x / y de la pantalla
        x = (self.m[0].width-WIDTH)/2
        y = (self.m[0].height-HEIGHT)/2

        #Dar dimensiones y ubicacion a la ventana
        w.geometry('%dx%d+%d+%d'% (WIDTH,HEIGHT,x,y))

         #Llamada a la función a la ventana
        self.inicializar_frame(w, WIDTH, HEIGHT, self.m)
       
        ##Crear y agregar widgets
        #wid = Window(w, WIDTH, HEIGHT, self.m)
        
        w.mainloop() 
    
    def inicializar_frame(self, w, WIDTH, HEIGHT, m):
        # Crear frame principal
        frame_principal = ttk.Frame(w, width=670, height=470,relief=tk.GROOVE, borderwidth=5)
        #Empaquetar el frame a la ventana raíz, con un margen de 'x'=15 y en 'y'=15
        frame_principal.pack(fill="both", expand=1, padx=15, pady=15)
        Window(frame_principal,WIDTH, HEIGHT, m, w)


    

Main()