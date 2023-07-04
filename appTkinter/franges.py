import os
import re
import time
import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import matlib as mt

from Trigger import Trigger
from capturaes import CapturaEs


class Franges():
    global num_imgn
    num_imgn = 0

    def __init__(self, monitores, parametros):
        self.m = monitores
        self.a = float (parametros[0])
        self.b = float(parametros[1])
        self.t= float (parametros[2])
        self.desc = parametros[3]
        self.etiqueta = parametros[4]
        #self.tabla = tabla
        
        self.m1 = self.m[1] #monitor 2
        #self.generar_franjas(m1)
        self.generar_projection()

    def phi_en(self, a, b, wid,hei, t):
        ''' Calcular 4 imagenes y phi de cada factor'''
        #Crear matrices con las dimensiones del proyector
        x = np.linspace(1, wid, wid, endpoint=True)
        y = np.linspace(1, hei, hei, endpoint=True)

        x_, y_ = np.meshgrid(x,y)
        
        w = 2*np.pi/t
        i_1 = a + b * np.cos(w*x_)
        i_2 = a + b * np.cos(w*x_ + np.pi/2)
        i_3 = a + b * np.cos(w*x_ + np.pi)
        i_4 = a + b * np.cos(w*x_ + 3/2 * np.pi)
        
        print(i_1.shape)
        
        i_s = [i_1, i_2, i_3, i_4]
        self.i_test = i_1 # i de prueba

        print('Calculando Phi con a: %d - b: %d - t: %d' % (a,b,self.t))

        return wid,hei, i_s

    def generar_franjas(self,m1):
        '''Generar franjas'''
        wid, hei, i_s, self.i_test = self.phi_en(self.a,self.b, m1.width,m1.height, self.t)
        #print(len(self.list_tmp))
        #print(self.list_tmp)
        
        
    def generar_projection(self):
        #obtener resolución de monitor 1
        m0 = self.m[0] #monitor 1
        m1 = self.m[1] #monitor 2
        print('Resolución Monitor1: ', m0 )
        print('Resolución Monitor2: ', m1 )
        self.win_top = tk.Toplevel()
        self.win_top.focus_set()
        #wi, he = (self.w.winfo_screenwidth()/2), self.w.winfo_screenheight()/2
        self.win_top.geometry('%dx%d+%d+0' % (m1.width, m1.height, m0.width )) #ubicar la ventana en el proyector
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

        

    def show_i_test(self):
        self.phi_en(self.a,self.b, self.m1.width,self.m1.height, self.t)
        plt.axes([0.05, 0.05,0.9,0.9])
        plt.imshow(self.i_test, cmap='gray')
        plt.axis('off')
        self.canvas.draw()
        self.win_top.update()

    def show_i_s(self):
        '''Generar franjas'''
        c = CapturaEs()
        t = Trigger()
        wid, hei, i_s = self.phi_en(self.a,self.b, self.m1.width,self.m1.height, self.t)
        for n  in range(len(i_s)):
                self.etiqueta.set('No. de patron de franjas: '+str(n))
                plt.axes([0.05, 0.05,0.9,0.9])
                # mostrar franjas
                plt.imshow(i_s[n], cmap='gray')
                plt.axis('off')
                self.canvas.draw()
                self.win_top.update()
                #print(' ALGO')
                time.sleep(3)
                c.main(n,self.desc,self.t)
                
                plt.clf()
                
                
                print(n)

    def capture_all_images(self, resolution):
        global num_imgn
        num_imgn += 1 #aumentar una unidad para nombrar la imagen
        #Crear objeto de clase para captura de imágenes
        t = Trigger()
        
        try:
            os.chdir('Capturas') #Guardar en carpeta las imagenes
        except:
            pass
        #t.main('hola', resolution)
        for n  in range(len(self.list_tmp)):
                for i in range(0, 4):
                    #mostrar franjas
                    plt.imshow(self.list_tmp[n][2][i], cmap='gray')
                    self.canvas.draw()
                    self.win_top.update()
                    
                    #construir nombre del archivo
                    name_file = str(i)+'-f' + str(self.w1) + str(self.list_tmp[0][3])
                    #hacer captura
                    t.main(name_file, resolution)
                    
                    #limpiar figura
                    plt.clf()
                    plt.axis('off')
                    plt.axes([-0.5, -0.5,2,2.5])

    def clean_table(self):
        # Si hay elementos en la lista, limpiarla, y colocar los nuevos elementos
            if self.tabla.get_children():
                # Se obtienen los id's de todos los items que se encuentran en la lista
                ids_items = self.tabla.get_children()
                # Por cada id se obtienen los valores de cada item
                for id_item in ids_items:
                    self.tabla.delete(id_item)

    
