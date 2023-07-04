import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm 
import random

class Fequidis:
    def __init__(self, pxy, f, a_b, w, rui, N, delta) -> None:
        self.px = pxy[0]
        self.py = pxy[1]
        self.a =  a_b[0]
        self.b =  a_b[1]
        self.f = f
        self.w = w
        self.rui = rui
        self.N = N
        self.t = (np.arange(1, N+1) - 1) * delta + 1
        
        wrapps = self.generate_images()
        unwrapps = self.unwrapping(wrapps)
        self.recover(unwrapps)

    
    def generate_images(self):
        wrappings = np.zeros((self.py, self.px, self.N)) #Crear lista con ceros 
        i = 0 #indice temporal
        #Desplazamiento de cuatro pasos
        alpha = [0, np.pi/2, np.pi, 3/2 * np.pi]
        for k in range(0, self.N):
            #Generar imágenes con sus respectivos desplazamientos
            I1 = self.a + self.b * np.cos( (self.w + self.f) * self.t[k] + self.rui + alpha[0])
            I2 = self.a + self.b * np.cos( (self.w + self.f) * self.t[k] + self.rui + alpha[1])
            I3 = self.a + self.b * np.cos( (self.w + self.f) * self.t[k] + self.rui + alpha[2])
            I4 = self.a + self.b * np.cos( (self.w + self.f) * self.t[k] + self.rui + alpha[3])

            #envolver imágenes y guardarlas en lista
            wrappings[:,:,i] = np.arctan2(I4-I2, I1-I3)          
            i+=1
        #fig1 = plt.figure(figsize=(6,6))
        #a = fig1.add_subplot(1,1,1)
        #plt.imshow(wrappings[:,:,i],cmap='gray')
        #plt.show()
        return wrappings
    
    def unwrapping(self, wrapps):
        #recuperar tamaño de la lista
        unwrs = np.zeros((self.py, self.px))

        #recorrer por pixelxpixel
        for i in range(self.py):
            for j in range(self.px):
                #desenvolver con método
                pu = self.equidistant(wrapps[i][j][:])
                #minimizar el error con minimos cuadrados
                pu = self.min_qua(pu)
                unwrs[i][j] = pu [0]

        return unwrs
    
    def equidistant(self,wrappings):
        #inicializar
        k=2
        N = len(wrappings)
        pu= np.zeros((N)) #(20,)
        pu[0] = wrappings[0]
        
        while k <N+1:
             term1 = pu[k-2] / self.t[k-2]  * self.t[k-1]
             term2 = wrappings[k-1] - pu[k-2]/ self.t[k-2] * self.t[k-1]
             pu[k-1] = term1 + np.arctan2(np.sin(term2), np.cos(term2))
             k+=1
        
        return pu
    
    def recover(self, unwrapps):
        res = np.zeros((self.py, self. px))
        obj2 = np.zeros((self.py, self. px))
        for i in range(self.py):
            for j in range(self.px):
                res[i][j] = unwrapps[i][j] - self.w[i][j]
                if res [i][j] < 0 or res [i][j]>=10:
                        res = 0
                    
                obj2[i][j] =res # np.rad2deg( res[i][j])

        x = np.linspace(-0.8*np.pi,0.8*np.pi,self.px,  endpoint=True)
        y = np.linspace(-0.8*np.pi,0.8*np.pi,self.py,  endpoint=True)

        x_, y_ = np.meshgrid(x, y)

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        surf = ax.plot_surface(x_, y_,obj2, cmap=cm.autumn, linewidth=0, antialiased = False)
        plt.show()

    def min_qua(self, wt):
        n = len(wt)
        y = wt
        #x =  (np.arange(1, n+1) - 1)*2 +1#crear vector de tk
        #Pendiente, número de unidades que aumenta y por cada unidad de x
        num = n*np.sum(self.t*y) - np.sum(self.t) * np.sum(y)
        den = n*np.sum(self.t**2) -( np.sum(self.t) ** 2)
        m = num/den
        #Ordenada al origen; intersección y; punto donde la recta corta el
        #eje ; valor de y cuando x =0
        num_b =  np.sum(y)* np.sum(self.t**2) - np.sum(self.t)*np.sum(self.t*y)
        dem_b = n*np.sum(self.t**2) -( np.sum(self.t) ** 2)
        b = num_b/dem_b
        #Coeficiente de correlación; varia de 0 a 1; nos dice qué tan bien la recta
        #se ajusta a los puntos experimentales; entre más cerca de 1, mayor es la bondad de ajuste
        num_r = n*np.sum(self.t*y) - np.sum(self.t) * np.sum(y)
        dem_r = np.sqrt( (n*np.sum(self.t**2) - np.sum(self.t)**2) * (n*np.sum(y**2) - np.sum(y)**2) )
        r = num_r / dem_r

        return [m,b,r]


####################################################################################
pixeles = [600, 400] #(pixeles, pixeles)

x = np.linspace(-0.8*np.pi,0.8*np.pi,pixeles[0],  endpoint=True)
y = np.linspace(-0.8*np.pi,0.8*np.pi,pixeles[1],  endpoint=True)

x_, y_ = np.meshgrid(x, y)
x0 = np.mean(x_)
y0 = np.mean(y_)

## función g
f =  0.2 * np.exp(- ((x_ - x0)**2 +  (y_ - y0)**2) / (2 * np.var(x_)))

w =  x_#x_ /np.pi

#print(g)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
surf = ax.plot_surface(x_, y_,w, cmap=cm.autumn, linewidth=0, antialiased = False)

a_b = [1, 1]

rui = np.random.randn(pixeles[1], pixeles[0]) * 0

#Se generan las imagenes en el tiempo t= 1,2,... N
N = 20 # t= 1,2,3, ... N
delta = 2

Fequidis(pixeles, f, a_b, w, rui, N, delta)