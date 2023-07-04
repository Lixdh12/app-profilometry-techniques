import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import tkinter.font as tkFont
from screeninfo import get_monitors

class ReconstruirTemporal():
    def __init__(self, frame, muestras, canvas, ax):
        super().__init__()
        self.frame = frame #Vincular la ventana principal, con la ventana del progress bar
        self.N = muestras #numero de muestras
        self.canvas = canvas #canvas para dibujar el grafico
        self.axr = ax
        
        self.choose_folder()
        self.read_imgs()
        self.reconstruction()

    def choose_folder(self):
        #Selección de carpeta de imágenes del objeto
        car = filedialog.askdirectory(title='Selecciona carpeta del objeto') #selección de carpeta
        if car=='':
            os.chdir(car)
        self.car_obj=car+'/'#car.getcwd()

        #Selección de carpeta de imágenes del plano
        car = filedialog.askdirectory(title='Selecciona carpeta del plano') #selección de carpeta
        if car=='':
            os.chdir(car)
        self.car_pla=car+'/'#os.getcwd()
        #print(self.car_obj, self.car_pla)
    
    def read_imgs(self):
        #selección de ROI
        print(self.car_obj+'t'+str(1)+'-i'+str(0)+'.png')
        #i = cv2.imread(self.car_obj+str(1)+'08'+str(0)+'.png',0)
        i = cv2.imread(self.car_obj+'t'+str(1)+'-i'+str(0)+'.png',0)
        r = cv2.selectROI('ROI', i,False,False)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()

        #Iniciar el progress Bar
        self.progressbar() #Inicializar bar
        self.bar.start() #comenzarlo
        self.label_des.set('Leyendo imágenes') #cambiar etiqueta
        self.child_window.update_idletasks() #actualizar ventana
        self.child_window.update()
        

        #selección de pixeles
        self.px = abs(int(r[0]) - int(r[0]+r[2]))
        self.py = abs(int(r[1]) - int(r[1]+r[3]))
        
        #Crear lista de imagenes
        self.list_obj = np.zeros((self.py,self.px,(self.N*4))) #lista para el objeto
        self.list_pla = np.zeros((self.py,self.px,(self.N*4))) #lista para el plano

        #Cargar y guardar imagenes en listas
        c= 0
        for t in range(1,self.N+1):
            for i in range(4):
                #guardar imagenes del objeto
                #self.list_obj[:,:,c] = cv2.imread(self.car_obj+str(t)+'08'+str(i)+'.png',0)[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                self.list_obj[:,:,c] = cv2.imread(self.car_obj+'t'+str(t)+'-i'+str(i)+'.png',0)[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                #guardar imagenes del plano
                #self.list_pla[:,:,c] = cv2.imread(self.car_pla+str(t)+'08'+str(i)+'.png',0)[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                self.list_pla[:,:,c] = cv2.imread(self.car_pla+'t'+str(t)+'-i'+str(i)+'.png',0)[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                #aumentar contador
                c += 1 
    def reconstruction(self):
        self.label_des.set('Reconstrucción en progreso ...') #Actualizar ventana del bar
        self.child_window.update_idletasks()
        self.child_window.update()
    #Recuperar y Desenvolver la fase del objeto y el plano
        obj= self.recover(self.list_obj, self.N)
        pla = self.recover(self.list_pla, self.N)
        #Lista para recuperar solo el objeto
        #objeto= np.zeros((py,px))     
        #objeto= pla - obj
        objeto= np.zeros((self.py,self.px))
        obj2= np.zeros((self.py,self.px))
        for i in range(self.py):
                for j in range(self.px):
                    res = - obj[i][j] + pla[i][j]
                    objeto[i][j] = res #magnitud del gradiente
                    
                    if res < 0 or res >=10:
                        res = 0
                    
                    obj2[i][j] = res
     

        
        self.bar.stop() #Detener bar
        self.child_window.destroy() #Destruir ventana del bar
        #Crear matrices con las dimensiones del proyector
        X, Y = np.meshgrid(np.arange(self.px), np.arange(self.py))
        self.axr.clear()
        #fig = plt.figure()
        #ax = fig.add_subplot(projection='3d')
        self.axr.plot_surface(Y, X, obj2, cmap=cm.YlGnBu, linewidth=0, antialiased = False)
        #self.axr.set_axis_off()
        #self.axr.set_xlabel('x')
        #self.axr.set_ylabel('y')
        #self.axr.set_zlabel('img')
        self.axr.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.axr.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.axr.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # make the grid lines transparent
        self.axr.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        self.axr.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        self.axr.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

        self.canvas.draw()

    
    def recover(self,lista, tiempo):
        self.label_des.set('Recuperando la fase envuelta y desenvolviendo...') #Actualizar etiqueta del bar
        self.child_window.update_idletasks() #Actualizar ventana del bar
        self.child_window.update()
        lista = lista.astype(np.float64)
        #recuperar forma de la lista
        sx, sy, N = lista.shape[0], lista.shape[1], lista.shape[2]
        t = tiempo
        img = np.zeros((sx, sy))
        #Pixel x pixel recuperar las imagenes y fases
        for col in range(sx):
            for fil in range(sy):
                cont = 0
                y1, y2, y3, y4 = np.zeros((t,)), np.zeros((t,)), np.zeros((t,)), np.zeros((t,))
                for ind in range(0, N, 4):
                #obtener imagenes i1,i2,i3,i4 
                    y1[cont] = lista[col, fil, ind]
                    y2[cont] = lista[col, fil, ind+1]
                    y3[cont] = lista[col, fil, ind+2]
                    y4[cont] = lista[col, fil, ind+3]
                    
                    cont += 1
                
                n = len(y1)
                ps = np.zeros((n,))
                
                #recuperar la fase
                #operaciones con arrays
                num = y4 - y2
                den = y3 - y1
                ps = np.arctan2(num, den)
                #rint(np.shape(ps))
                #    aux = ps[i]
    
                #desenvolver fases
                ps = self.phase_unwrapping(ps, tiempo)
                #Ajuste con minimos cuadrados
                p = self.min_cuadrados(ps)
                img[col, fil] = p[0]
        
        #print (cont)
        return img
    
        #Desenvolver fase
    def phase_unwrapping(self,phase_wra, tiempo):
        self.child_window.update_idletasks() #Actualizar ventana del bar
        self.child_window.update()
        '''Parametros: 
            phase_wra - fase envuelta, forma (x, y)
        Return:
            list_unwra - lista de pixeles desenvueltos
        '''
        N = len(phase_wra) #muestras temporales
        phase_unw = np.zeros((N)) #(10,)
        phase_unw[0] = phase_wra[0]
        Kp = 0
        #for j in range(0, pixeles):
        for k in range(1, N):
                #Calcular la diferencia entre dos muestras y su signo
                diffe = (phase_wra[k]-phase_wra[k-1])/ (2*np.pi)
                signo = np.sign(diffe)
                #Verificar si wt es positiva o negativa
                #para hacer el ajuste
                if np.abs( diffe  ) > 0.7:
                    #Cuando wt es pendiente positiva
                    if signo == -1:
                        Kp = Kp + 2 * np.pi
                        phase_unw[k] =  phase_wra[k] + Kp
                    #Cuando wt es pendiente negativa
                    if signo == 1:
                        Kp = Kp - 2 * np.pi
                        phase_unw[k] =phase_wra[k] + Kp
                else:
                    phase_unw[k] = phase_wra[k] + Kp
        
        # Multiplicar por el tiempo
        phase_unw*= N
        return phase_unw

    #Ajuste de minimos cuadrados
    def min_cuadrados(self,wt):
        n = len(wt)
        y = wt
        x =  np.arange(0, n)
        #Pendiente, número de unidades que aumenta y por cada unidad de x
        num = n*np.sum(x*y) - np.sum(x) * np.sum(y)
        den = n*np.sum(x**2) -( np.sum(x) ** 2)
        m = num/den
        #Ordenada al origen; intersección y; punto donde la recta corta el
        #eje ; valor de y cuando x =0
        num_b =  np.sum(y)* np.sum(x**2) - np.sum(x)*np.sum(x*y)
        dem_b = n*np.sum(x**2) -( np.sum(x) ** 2)
        b = num_b/dem_b
        #Coeficiente de correlación; varia de 0 a 1; nos dice qué tan bien la recta
        #se ajusta a los puntos experimentales; entre más cerca de 1, mayor es la bondad de ajuste
        num_r = n*np.sum(x*y) - np.sum(x) * np.sum(y)
        dem_r = np.sqrt( (n*np.sum(x**2) - np.sum(x)**2) * (n*np.sum(y**2) - np.sum(y)**2) )
        # Here we check error
        if num_r and dem_r:
            r = num_r / dem_r

            return [m,b,r]
        
        return [0,0,0]

    def progressbar(self):
        # Crear ventana hija para mostrar el progreso de la redimensión
        self.child_window = tk.Toplevel(self.frame)
        # Configurar ventana hija
        self.child_window.title("Reconstrucción")
        
       
        # self.child_window.geometry('350x100')
        self.child_window.grab_set()
        self.child_window.transient(self.frame)
        self.child_window.resizable(width=False, height=False)
        
        #Obtener los datos de los monitores conectados
        self.m = get_monitors()
        #Obtener las dimensiones del monitor principal
        WIDTH = (self.m[0].width)
        HEIGHT = (self.m[0].height)
        # Dimensiones de la ventana hija
        w = 500
        h = 150
        # Determinar la anchira y longitud de la pantalla
        sw = self.child_window.winfo_screenwidth()
        sh = self.child_window.winfo_screenheight()
        # Calcular las coordenadas x / y
        x = (WIDTH- w) / 2
        y = (HEIGHT - h) / 2
        # Dar dimensiones y ubicacion a la ventana
        self.child_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.label_des = tk.StringVar()
        self.label_des.set('Reconstruyendo, espere.')
        # Agregar descripcion
        self.fon = tkFont.Font(family="Arial", size=13, weight="bold")
        label_description = tk.Label(self.child_window, textvariable=self.label_des, font=self.fon)
        label_description.pack(expand=1)
        self.bar = ttk.Progressbar(self.child_window, length=200, mode="indeterminate",
                                   takefocus=True)
        self.bar.pack(expand=1)
        #self.bar['value'] = 0
        #self.bar['maximum'] = self.N
    
    def progress_bar(self):
        self.current_value+=1
        self.bar['value'] = self.current_value

    # Detener el progressbar
    def stop_bar(self):
        self.bar.stop()
        self.bar['value'] = self.N

    def cancel(self):
        # Destruir la ventana
        self.child_window.destroy()
        raise StopIteration