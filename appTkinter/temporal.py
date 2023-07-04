'''Esta clase genera las imagenes en tiempo, las envuelve, desenvuelve, 
y aplica un ajuste con minimos cuadrados. Además, de calcular el error.
'''
#Importar modulos
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from matplotlib import cm


class Temporal():
    def __init__(self, e_t, a, b, w,N, rx, canvas, ax):
        self.e_t = e_t #opción elegida
        self.a = a #intensidad media
        self.b = b #intensidad modulada
        self.w = w #frecuencia
        self.N = N #número de muestras
        self.rx = [200,200] #resolución de la imagen
        self.canvas = canvas
        self.ax = ax

        if self.e_t == 1 :
            #si la opción es lineal
            self.lineal()
        else:
            self.expon()

    def lineal(self):
        x = np.linspace(-0.9*np.pi,0.9*np.pi,(self.rx[0],self.rx[1]),  endpoint=True)
        y = np.linspace(-0.9*np.pi,0.9*np.pi,(self.rx[0],self.rx[1]),  endpoint=True)

        x_, y_ = np.meshgrid(x, y)
        x0 = np.mean(x_)
        y0 = np.mean(y_)
        ## función g
        g =  0.2 * np.exp(- ((x_ - x0)**2 +  (y_ - y0)**2) / (2 * np.var(x_)))
        self.w =   x_ /np.pi
        print('Generando imagenes de '+str(self.rx[0])+'x'+str(self.rx[1]))
        self.generar_images([self.a, self.b], self.w, g,0,self.N, self.rx)

    def expon():
        pass

    def generar_images(self,a_b,w, g, rui, N, rx):
        list_wra = np.zeros((rx[0],rx[1],N))
        tim = np.arange(0, N) #0.2 
        
        #definir los desplazamientos
        alpha = [0, np.pi/2, np.pi, 3/2 * np.pi]
        for t in range(1, N):
            #Generar las 4 imágenes con sus respectivos desplazamientos
            i1 = a_b[0] + a_b[1] * np.cos( (w+ g)*t  + rui + alpha[0] )
            i2 = a_b[0] +a_b[1] * np.cos( (w+ g)*t + rui + alpha[1] )
            i3 = a_b[0] +a_b[1] * np.cos( (w+ g)*t  + rui + alpha[2] )
            i4 = a_b[0] + a_b[1] * np.cos( (w+ g)*t  + rui + alpha[3] )

            #Envolver las imagenes; se obtiene una forma (200, 200)
            list_wra[:,:,t] = np.arctan2(i4-i2, i1-i3)
            #Desenvolver las imagens; se obtiene una forma (200,200)
            #unwrapp = phase_unwrapping(wrapp)
            #Agregar a una lista en cada t=1,2,3, N y que la función la devuelva
            #list_unwra[:,:,t]=unwrapp

        
        recu = np.zeros((rx[0],rx[1]))

        for i in range(rx[0]):
            for j in range(rx[1]):
                #plt.plot(list_wra[0][j], '-o', color='blue')
                
                #desenvolver cada pixel en el tiempo
                tmp1 = self.phase_unwrapping(list_wra [i][j][:])
                #p = np.polyfit(tim, tmp1, 1,)
                
                q = self.min_cuadrados(tmp1)            
                recu[i][j] = q[0]

        #print(q)
        gaus = np.zeros((rx[0],rx[1]))
        #obtener objeto por cada pixel
        for i in range(rx[0]):
            for j in range(rx[1]):
                gaus[i][j] = recu[i][j] - w[i][j]

        return gaus

    #Desenvolver fase
    def phase_unwrapping(self,phase_wra):
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
        return phase_unw

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
        r = num_r / dem_r

        return [m,b,r]