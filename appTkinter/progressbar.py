import tkinter as tk
from tkinter import ttk

class ShowProgressBar:
    def __init__(self):
        pass
    #Crear ventana hija
    def create_window(self):
        # Crear ventana hija para mostrar el progreso de la redimensión
        self.child_window = tk.Toplevel(self.father_window)
        # Configurar ventana hija
        self.child_window.title("Recortando")
        # Centrar ventana hija
        self.centrar_ventana()
        # self.child_window.geometry('350x100')
        self.child_window.grab_set()
        self.child_window.transient(self.father_window)
        self.child_window.resizable(width=False, height=False)

    def center_window(self):
        #Dimensiones de la ventana
        w = 350
        h = 100
        #Determinar la anchira y longitud de la pantalla
        sw = self.child_window.winfo_screenwidth()
        sh = self.child_window.winfo_screenheight()
        #Calcular las coordenadas x / y
        x = (sw-w)/2
        y = (sh-h)/2
        #Dar dimensiones y ubicacion a la ventana
        self.child_window.geometry('%dx%d+%d+%d'% (w,h,x,y))

    #Agregar widgets a la ventana hija
    def add_widgets(self):
        # Agregar descripcion
        label_description = tk.Label(self.child_window, text="Reconstruyendo, espere.")
        label_description.pack()
        # Configurar el progressbar
        self.bar = ttk.Progressbar(self.child_window, length=200, mode="determinate")
        self.bar.pack()
        self.bar['value'] = 0
        self.bar['maximum'] = 100

        # Agregar botón para cancelar la redimensión
        self.button_cancel = tk.Button(self.child_window, text="Cancelar", command=self.cancel)
        self.button_cancel.config(font=("Arial", 10, "bold"))
        self.button_cancel.pack(pady=10)

    #Establecer valores a usar en la ventana hija
    def set_values(self):
        pass
    #Comenzar el avance del progress según los datos dados
    def start_progressbar(self):
        pass
    #Destruir laa ventana hija
    def end_progressbar(self):
        pass
    #Cancelar proceso
    def cancel_progressbar(self):
        pass
    #Agregar widgets a la ventana hija, agregar un textarea
    def add_widgets_plus(self):
        pass
