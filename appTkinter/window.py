import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext as st
import tkinter.font as tkFont
from ftempo import FrangeTempo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure
from acquire_display import AcquireDisplay
from reconstruir import Reconstruir
from reconstruir_ELTS import ReconstruirELTS
from reconstruir_temp import ReconstruirTemporal

from temporal import Temporal
from franges import Franges

class Window(ttk.Frame):
    def __init__(self, win, w, h, m, windowmain):
        #tk.Frame.__init__(self, win)
        self.win = win #window
        self.w = w #width
        self.h = h #height
        self.m = m #monitors
        self.frame = windowmain #ventana principal
              
        self.franges()
        self.desenvolvimiento()
        self.pro_capt()
        self.re()
        self.vista()
        self.recons()
        #intentar iniciar la camra
        try:
            self.mos.set('Cámara conectada')
            self.lb8.config(foreground='black')
            self.acquire_display = AcquireDisplay(self.l_vi , self.canvas, self.ax, 0)
            self.acquire_display.live_camera()
        except:
            self.mos.set('Cámara desconectada')
            self.lb8.config(foreground='black')
            print('Camara no detectada')
        
    
    def franges(self):
        #Definir font para las etiquetas de las secciones

        #Definir estilos para botones
        self.s = ttk.Style()
        self.s.configure("Bold.TLabel", font=("TkDefaultFont", 9, "bold"))
        
        self.fon = tkFont.Font(family="Arial", size=13, weight="bold")
        self.fr = ttk.Frame(self.win)
        self.fr.grid(column=0, row=0)
    
        label = ttk.Label(text="Generación de Franjas", style='Bold.TLabel')
        self.l_fr=ttk.LabelFrame(self.fr, labelwidget=label)
        self.l_fr.grid(column=0, row=0, padx=5, pady=1)

        #Entrada para la intensidad media A
        self.lb1=ttk.Label(self.l_fr, text="Intensidad media:")
        self.lb1.grid(column=0, row=0, padx=4, pady=4)
        self.a=tk.StringVar(value="127")
        self.e_a=ttk.Entry(self.l_fr, textvariable=self.a, justify='center', font=('Arial', 12, 'normal'), width=10)
        self.e_a.grid(column=1, row=0, padx=4, pady=4)

        #Entrada para la intensidad modulada B
        self.lb_2=ttk.Label(self.l_fr, text="Amplitud:")
        self.lb_2.grid(column=0, row=1, padx=4, pady=4)
        self.b=tk.StringVar(value="127")
        self.e_b=ttk.Entry(self.l_fr, textvariable=self.b, justify='center', font=('Arial', 12, 'normal'), width=10)
        self.e_b.grid(column=1, row=1, padx=4, pady=4)

        #Entrada para la frecuencia o periodo W
        self.lb_3=ttk.Label(self.l_fr, text="Frecuencia:")
        self.lb_3.grid(column=0, row=2, padx=4, pady=4)
        self.w=tk.StringVar(value="10")
        self.e_w=ttk.Entry(self.l_fr, textvariable=self.w, justify='center', font=('Arial', 12, 'normal'), width=10)
        self.e_w.grid(column=1, row=2, padx=4, pady=4)

        #Entrada para la resolución de las imágenes
        self.lb_4=ttk.Label(self.l_fr, text="Resolución:")
        self.lb_4.grid(column=0, row=3, padx=4, pady=4)
        #self.r=tk.StringVar()
        #agregar select resolución
        #comprobar si hay 2do monitor
        
        try:
            self.resolution = [self.m[1].width,self.m[1].height]
            self.combo_sx = ttk.Combobox(self.l_fr, width=12,justify='center', font=('Arial', 12, 'normal'),
                values= [str(self.m[1].width)+'x'+str(self.m[1].height), "1024x768","800x600"] # "1280x1024",
            )
            print('2da pantalla detectada ...')
        except:
            self.resolution = [self.m[0].width,self.m[0].height]
            self.combo_sx = ttk.Combobox(self.l_fr, width=12,justify='center', font=('Arial', 12, 'normal'),
                values= [str(self.m[0].width)+'x'+str(self.m[0].height), "1024x768","800x600"] # "1280x1024",
            )
            print('Solo existe una pantalla ...')
        self.combo_sx.current(0)
        self.combo_sx.bind('<<ComboboxSelected>>', self.selection_changed)
        self.combo_sx.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.bt = ttk.Button(self.l_fr, text='Previsualizar', command=self.vista_previa)
        self.bt.grid(column=1, row=4,)
    
    def desenvolvimiento(self):
        self.de = ttk.Frame(self.win)
        self.de.grid(column=1, row=0)
        label = ttk.Label(text="Desenvolvimiento", style="Bold.TLabel")
        self.l_de=ttk.LabelFrame(self.de, labelwidget=label)        
        self.l_de.grid(column=0, row=0, padx=5, pady=1)

        self.e_t = 0
        self.lb5=ttk.Label(self.l_de, text="Espacial/temporal:")
        self.lb5.grid(column=0, row=0, padx=4, pady=4)
        self.co_et = ttk.Combobox(self.l_de,justify='center', font=('Arial', 10, 'normal'), width=12,
                values= ['Espacial', "Temporal"], state='readonly'
            )
        self.co_et.current(0)
        self.co_et.bind('<<ComboboxSelected>>', self.select)
        self.co_et.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5, columnspan=2)

        self.muest = 0
        self.lb6=ttk.Label(self.l_de, text="Muestreo:")
        self.lb6.grid(column=0, row=1, padx=4, pady=4)
        self.co_muestreo = ttk.Combobox(self.l_de,justify='center', font=('Arial', 10, 'normal'), width=12,
                values= ['Lineal', "ELTS"], state='disabled'
            )
        self.co_muestreo.current(0)
        self.co_muestreo.bind('<<ComboboxSelected>>', self.select_muestreo)
        self.co_muestreo.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5, columnspan=2)

        self.lb7=ttk.Label(self.l_de, text="Número de muestreos:", state='disabled')
        self.lb7.grid(column=0, row=2, padx=4, pady=4)
        self.n=tk.StringVar(value='1')
        self.e_n=ttk.Entry(self.l_de, textvariable=self.n, justify='center', font=('Arial', 12, 'normal'),width=10, state='disabled')
        self.e_n.grid(column=1, row=2, padx=4, pady=4,  columnspan=2)

        self.lb9=ttk.Label(self.l_de, text="Número de pasos:", state='disabled')
        self.lb9.grid(column=0, row=3, padx=4, pady=4)
        self.n_p=tk.StringVar(value='1')
        self.e_p=ttk.Entry(self.l_de, textvariable=self.n_p, justify='center', font=('Arial', 12, 'normal'),width=10, state='disabled')
        self.e_p.grid(column=1, row=3, padx=4, pady=4,  columnspan=2)
        
    #Proyectar y capturar los patrones de franjas
    def pro_capt(self):
        self.po = ttk.Frame(self.win)
        self.po.grid(column=2, row=1)
        label = ttk.Label(text="Captura y reconstrucción", style="Bold.TLabel")
        self.l_po=ttk.LabelFrame(self.po, labelwidget=label)
        
        self.l_po.grid(column=0, row=0, padx=5, pady=1)

        
        self.bttn_play = ttk.Button(self.l_po, text='Empezar', command=self.started)
        self.bttn_play.pack()
        
        #etiqueta que mostrará el # de muestra proyectado
        self.mos = tk.StringVar()
        self.lb8=ttk.Label(self.l_po, textvariable=self.mos, font=self.fon)
        self.lb8.pack()#grid(column=0, row=3, padx=4, pady=4, columnspan=2)
    
    #Sección para la reconstrucción del objeto con las imágenes ya almacenadas
    def re(self):
       
        label = ttk.Label(text="Reconstrucción", style="Bold.TLabel")
        self.l_rec=ttk.LabelFrame(self.po, labelwidget=label)
        
        self.l_rec.grid(column=0, row=1, padx=5, pady=1)

        
        self.bttn_rec = ttk.Button(self.l_rec, text='Empezar', command=self.started_reconstruction)
        self.bttn_rec.pack()
        
    #Visualización de la cámara para la previsualización
    def vista(self):
        self.vi = ttk.Frame(self.win)
        self.vi.grid(column=0, row=1,columnspan=2,ipadx=5, ipady=5)
        label = ttk.Label(text="Vista previa", style="Bold.TLabel")
        self.l_vi = ttk.LabelFrame(self.vi, labelwidget=label)
        self.l_vi.grid(column=0, row=0, padx=5, pady=1)

        #Crear figura para agregar el canvas
        self.figi = Figure(figsize=(6, 4),  dpi=100)
        self.ax = self.figi.add_subplot()
        self.ax.set_yticks([])
        self.ax.set_xticks([])
         
        #Crear canvas para dibujar la imagen de la camara
        self.canvas = FigureCanvasTkAgg(self.figi, master=self.l_vi)
        #bbox = canvas.bbox(tk.ALL)
        #canvas.config(width=bbox[2] - bbox[0])
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    #Espacio para el grafico de la reconstrucción del objeto
    def recons(self):
        self.re = ttk.Frame(self.win)
        self.re.grid(column=4, row=0,rowspan=2,ipadx=5, ipady=5)
        
        label = ttk.Label(text="Vista de reconstrucción", style='Bold.TLabel')

        self.l_re = ttk.LabelFrame(self.re, labelwidget=label)
        self.l_re.grid(column=0, row=0, padx=5, pady=1)

        #Crear figura para agregar el canvas
        fig = Figure()
        self.axr = fig.add_subplot(projection='3d')

         #Crear canvas para dibujar la imagen de la camara
        self.canv = FigureCanvasTkAgg(fig, master=self.l_re)
        self.canv.draw()
        self.canv.get_tk_widget().grid(row=0, column=0)
        
        #frame para toolbar
        toolbar_frame = tk.Frame(self.l_re)
        toolbar_frame.grid(row=1,column=0,columnspan=2)
        #Crear y agregar toolbar
        toolbar = NavigationToolbar2Tk(self.canv, toolbar_frame)
        toolbar.update()
        self.canv._tkcanvas.grid(row=0, column=0)

    #Proyección de franjas para la previsualización
    def vista_previa (self):
        #Destruir canvas
        #self.figi.clear()
        #self.canvas = None
        #Agregar previous camera
        #Proyección
        
        parametros = [self.a.get(), self.b.get(), self.w.get(), None, self.mos]
        franges = Franges(self.m, parametros)
        franges.show_i_test()
        
        #acquire_display = AcquireDisplay(self.l_vi , self.canvas, self.ax)

    def started_reconstruction(self):
        self.mos.set('Reconstruyendo, espere ...')
        self.lb8.config(foreground='green')

        '''Reconstruir con las imagenes ya guardadas de la técnica espacial'''
        if self.e_t == 0:
            #si es espacial
            #Crear objeto de la clase reconstruir
            re = Reconstruir()
            re.obtener_imagenes(self.canv, self.axr)
            
        elif self.e_t == 1 and self.muest==0:
            #try:
                ReconstruirTemporal(self.frame, int(self.n.get()),self.canv, self.axr)
            #except:
             #   messagebox.showinfo(message="Ingresa el número de muestras", title="ERROR")
        elif self.e_t == 1 and self.muest==1:
                ReconstruirELTS(self.frame,int(self.n.get()),int(self.e_p.get()),self.canv, self.axr)

        
        self.mos.set('Cámara conectada')
        self.lb8.config(foreground='black')

    def started(self):
        '''Comenzar la captura y reconstrucción'''
        #detener camara
        self.acquire_display.stop_camera=1

        #mostrar dialogo para avisar al usuario proyección del plano
        messagebox.showinfo(message="Verifica que el objeto esté sobre el plano", title="Alerta")

        if self.e_t == 0:
            #si es espacial
            print('Espacial')
            self.trigger_cam("pbj", self.mos)
            
        elif self.e_t == 1 and self.muest==0:
            #si es temporal y lineal
            print('Temporal:', self.muest)
            #mb.messagebox.showinfo(message="Coloca el objeto", title="¡Atención!")
            #
            #temp = Temporal(self.e_t, int(self.a.get()), int(self.b.get()),
            #                 float(self.w.get()),int(self.n.get()), self.resolution, self.canvas, self.axr)
            ft = FrangeTempo(self.m, [self.a.get(), self.b.get(), self.w.get(), self.n.get(),'obj',0 ])
            ft.generate(self.mos)
        
        #Proyectar y capturar con la técnica ELTS para el objeto
        elif self.e_t == 1 and self.muest==1:
            #si es temporal y lineal
            print('Temporal:', self.muest)
            #mb.messagebox.showinfo(message="Coloca el objeto", title="¡Atención!")
            #
            #temp = Temporal(self.e_t, int(self.a.get()), int(self.b.get()),
            #                 float(self.w.get()),int(self.n.get()), self.resolution, self.canvas, self.axr)
            ft = FrangeTempo(self.m, [
                self.a.get(), self.b.get(), self.w.get(),
                  self.n.get(),'obj', self.n_p.get()])
            ft.generate_equidis(self.mos)
        else:
            print(self.muest)

        #Mostrar dialogo para avisar al usuario proyección del objeto
        messagebox.showinfo(message="Retira el objeto del plano", title="Alerta")
        if self.e_t == 0:
            #si es espacial
            print('Espacial')
            self.trigger_cam("pln", self.mos)

            #mostrar dialogo para avisar al usuario proyección del objeto
            messagebox.showinfo(message="¡Imagenes capturadas! Selecciona las imágenes el objeto y después el plano", title="Alerta")
            #Crear objeto de la clase reconstruir
            re = Reconstruir()
            re.obtener_imagenes(self.canv, self.axr)
        
        #Proyectar y capturar con la técnica lineal para el plano
        elif self.e_t == 1 and self.muest==0:
            #si es temporal y lineal
            print('Temporal:', self.muest)
            #mb.messagebox.showinfo(message="Coloca el objeto", title="¡Atención!")
            #
            #temp = Temporal(self.e_t, int(self.a.get()), int(self.b.get()),
            #                 float(self.w.get()),int(self.n.get()), self.resolution, self.canvas, self.axr)
            ft = FrangeTempo(self.m, [self.a.get(), self.b.get(), self.w.get(), self.n.get(),'pla', 0 ])
            ft.generate_lineal(self.mos)
            messagebox.showinfo(message="¡Imagenes capturadas!", title="Alerta")
            try:
                self.mos.set('Reconstruyendo, espere ...')
                self.lb8.config(foreground='green')
                ReconstruirTemporal(self.frame,int(self.n.get()), self.canv, self.axr)
            except:
                self.mos.set('Algo salió mal')
                self.lb8.config(foreground='red')
        
        #Proyectar y capturar con la técnica ELTS para el plano
        elif self.e_t == 1 and self.muest==1:
            #si es temporal y lineal
            print('Temporal:', self.muest)
            #mb.messagebox.showinfo(message="Coloca el objeto", title="¡Atención!")
            #
            #temp = Temporal(self.e_t, int(self.a.get()), int(self.b.get()),
            #                 float(self.w.get()),int(self.n.get()), self.resolution, self.canvas, self.axr)
            ft = FrangeTempo(self.m, [
                self.a.get(), self.b.get(), self.w.get(),
                  self.n.get(),'pla', self.n_p.get()])
            ft.generate_equidis(self.mos)
            messagebox.showinfo(message="¡Imagenes capturadas!", title="Alerta")
            try:
                self.mos.set('Reconstruyendo, espere ...')
                self.lb8.config(foreground='green')
                ReconstruirELTS(self.frame,int(self.n.get()), int(self.n_p.get()), self.canv, self.axr)
            except:
                self.mos.set('Algo salió mal')
                self.lb8.config(foreground='red')
        #intentar iniciar la camra
        try:
            self.acquire_display = AcquireDisplay(self.l_vi , self.canvas, self.ax, 0)
            self.acquire_display.live_camera()
            self.mos.set('Cámara conectada')
            self.lb8.config(foreground='black')
        except:
            print('Camara no detectada')
        
        

         

    def trigger_cam(self, description, etiquet):
        #global num_imgn
        parametros = [self.a.get(), self.b.get(), self.w.get(), description, etiquet]
        franges = Franges(self.m, parametros)
        franges.show_i_s()

    def selection_changed(self,event):
        #De acuerdo a la resolución seleccionada
        selection = self.combo_sx.get() 
        #if selection == "1280x1024":
        #    w = 1280
        #    h = 1024
        if selection == str(self.w)+'x'+str(self.h):
            w = self.w
            h = self.h
        elif selection == "1024x768":
            w = 1024
            h = 768
        elif selection == "800x600":
            w = 800
            h = 600
        
        self.resolution = [w,h]
    
    def select(self,event):
        #De acuerdo la opción:
        # espacial -> 0
        # temporal -> 1
        selection = self.co_et.get() 
        if selection == 'Espacial':
            self.lb_3.config(state='enabled')
            self.e_w.config(state='enabled')
            self.lb6.config(state='disabled')
            self.co_muestreo.config(state='disabled')
            self.lb7.config(state='disabled')
            self.e_n.config(state='disabled')
            self.lb9.config(state='disabled')
            self.e_p.config(state='disabled')
            self.e_t = 0
        elif selection == "Temporal":
            print('seleccionado', selection)
            self.lb_3.config(state='disabled')
            self.e_w.config(state='disabled')
            self.lb6.config(state='enabled')
            self.co_muestreo.config(state='readonly')
            self.lb7.config(state='enabled')
            self.e_n.config(state='enabled')
            self.e_t = 1
        
    def select_muestreo(self,event):
        #De acuerdo la opción:
        # espacial -> 0
        # temporal -> 1
        selection = self.co_muestreo.get() 
        if selection == 'Lineal':
            self.lb9.config(state='disabled') #Etiqueta de número de pasos(ELTS)
            self.e_p.config(state='disabled') #Entry (ELTS)
            self.muest = 0
        elif selection == "ELTS":
            self.lb9.config(state='enabled') #Etiqueta de número de pasos(ELTS)
            self.e_p.config(state='enabled') #Entry (ELTS)
            self.muest = 1