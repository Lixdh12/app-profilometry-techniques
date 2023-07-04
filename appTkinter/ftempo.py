import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from capturar import Capturar

class FrangeTempo():
    def __init__(self, monitores, parametros):
        self.m = monitores
        self.a = float (parametros[0]) #intensidad media
        self.b = float(parametros[1]) #intensidad modulada
        self.w= float (parametros[2]) #omega
        self.N = int(parametros[3]) #numero de muestras
        self.objeto = parametros[4] #bandera para identificar que va primero
        self.delta = int(parametros[5]) #número de pasos
        #self.tabla = tabla

        #Color negro la etiqueta de la cuenta de imagenes
        #self.lb8.config(foreground='black')

        #guardar imagenes capturadas
        self.cap_img=[]
        #self.cap = Capturar()
        self.m1 = self.m[1] #monitor 2
        self.generar_projection()
        

    #Crear dimensiones del proyector
    def crear_dimen(self, wid,hei):
         #Crear matrices con las dimensiones del proyector
        x = np.linspace(-np.pi,np.pi, wid, endpoint=True)
        y = np.linspace(-np.pi,np.pi, hei, endpoint=True)
        #Crear mash
        self.x_, self.y_ = np.meshgrid(x,y)
        self.w = self.x_
    
    #Generar franjas en el tiempo
    def generate_lineal(self, etiqueta):
        self.etiqueta = etiqueta
        for t in range(1,self.N+1):
            i_s = self.gen_fran(t)
            self.show_imgs( i_s, t)
    
    #Generar franjas en el tiempo ELTS
    def generate_equidis(self, etiqueta):
        self.etiqueta = etiqueta
        T = (np.arange(1, self.N+1) - 1) * self.delta + 1
        for t in T:
            i_s = self.gen_ELTS(t)
            self.show_imgs( i_s, t)

    #Generar 4 patrones de franjas en un tiempo: n, n+1, n+2, ...N
    def gen_fran(self, t):
        ''' Calcular 4 imagenes y phi de cada factor'''
        print('Generando imágenes de t=', t)
        #fig = plt.figure()
        #plt.plot(self.w[100,:])
        #plt.show()
        #Generar las 4 imágenes con sus respectivos desplazamientos
        i_1 = self.a + self.b * np.cos(self.w*t)
        i_2 = self.a + self.b * np.cos(self.w*t + np.pi/2)
        i_3 = self.a + self.b * np.cos(self.w*t + np.pi)
        i_4 = self.a + self.b * np.cos(self.w*t + 3/2 * np.pi)
        
        #Agregar a una lista las imagenes generadas
        i_s = [i_1, i_2, i_3, i_4]
        return i_s
    
    #Generar 4 patrones de franjas en un tiempo en D pasos
    def gen_ELTS(self, t):
        ''' Calcular 4 imagenes y phi de cada factor'''
        print('Generando imágenes de t=', t)
        #fig = plt.figure()
        #plt.plot(self.w[100,:])
        #plt.show()
        #Generar las 4 imágenes con sus respectivos desplazamientos
        i_1 = self.a + self.b * np.cos(self.w*t)
        i_2 = self.a + self.b * np.cos(self.w*t + np.pi/2)
        i_3 = self.a + self.b * np.cos(self.w*t + np.pi)
        i_4 = self.a + self.b * np.cos(self.w*t + 3/2 * np.pi)
        
        #Agregar a una lista las imagenes generadas
        i_s = [i_1, i_2, i_3, i_4]
        return i_s
    

    def generar_projection(self):
        #obtener resolución de monitor 1
        m0 = self.m[0] #monitor 1
        self.m1 = self.m[1] #monitor 2
        #
        #Crear dimensiones del proyector en mash
        self.crear_dimen( self.m1.width,self.m1.height)

        print('Resolución Monitor1: ', m0 )
        print('Resolución Monitor2: ', self.m1 )
        self.win_top = tk.Toplevel()
        self.win_top.focus_set()
        #wi, he = (self.w.winfo_screenwidth()/2), self.w.winfo_screenheight()/2
        self.win_top.geometry('%dx%d+%d+0' % (self.m1.width, self.m1.height, m0.width )) #ubicar la ventana en el proyector
        self.win_top.overrideredirect(True)
        
        # figura que contendrá el grafico
        self.fig, self.axs = plt.subplots()
        plt.axis('off')
        plt.axes([-0.5, -0.5,2,2.5])
        # Crear el canvas de Tkinter
        # que contendrá el grafico
        self.canvas = FigureCanvasTkAgg(self.fig,
                                master=self.win_top)

        # Colocar en la ventana
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        #self.generar_franjas(m1)
        #self.i_s, self.phi = self.phi_en(self.a,self.b, m1.width,m1.height, self.t)
        #plt.imshow(self.phi, cmap='gray')

        self.win_top.update()

    #mostrar las imagenes generadas
    def show_imgs(self, i_s, t):
        
        cap = Capturar()
        '''Generar franjas'''
        for n  in range(len(i_s)):
                
                plt.axes([0.05, 0.05, 0.9 ,0.9])
                # mostrar franjas
                plt.imshow(i_s[n], cmap='gray', vmin=0, vmax=255)
                plt.axis('off')
                """ fig = plt.figure()
                im = i_s[n]
                plt.imshow(i_s[n] ,cmap='gray', vmin=0, vmax=255)
                plt.title('pri')
                plt.show() """
                
                
                self.canvas.draw()
                self.win_top.update()
               
                self.etiqueta.set('No. Muestra: '+str(t) + '\tNo. Patrón: '+str(n))
    
                self.cap_img.append([t,cap.main(n,t, self.objeto)])
                time.sleep(1)
                plt.clf()
                
                print(n)
        
        print(np.shape(self.cap_img))


    