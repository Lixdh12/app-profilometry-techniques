import cv2
import numpy as np
import tkinter as tk
import tkinter.filedialog as fd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class Reconstruir():
    def ___init___(self):
        print('estoy dento')
        

    def obtener_imagenes(self, canvas, ax):
        root = tk.Tk()
        filez = fd.askopenfilenames(parent=root, title='Choose a files of object')
        root.destroy()

        It=cv2.imread(filez[0])
        It = cv2.cvtColor(It, cv2.COLOR_BGR2GRAY)
        [nf,nc]=It.shape
        Phi=np.zeros((nf,nc,4))
        Phi[:,:,0]=It
        wx=np.zeros((nf,nc,4))
        for i in range(1,4):
            It=cv2.imread(filez[i])
            It = cv2.cvtColor(It, cv2.COLOR_BGR2GRAY)
            It=It.astype(np.float64)
            Phi[:,:,i]=It

        root = tk.Tk()
        filez = fd.askopenfilenames(parent=root, title='Choose a file of plane')
        root.destroy()
        for i in range(0,4):
            It=cv2.imread(filez[i])
            It = cv2.cvtColor(It, cv2.COLOR_BGR2GRAY)
            It=It.astype(np.float64)
            wx[:,:,i]=It

        print('Envolviendo ...')
        Phi_w=np.arctan2(Phi[:,:,3]-Phi[:,:,1],Phi[:,:,0]-Phi[:,:,2])
        wx_w = np.arctan2(wx[:,:,3]-wx[:,:,1],wx[:,:,0]-wx[:,:,2])
        #print(Phi_w)
        #plt.imshow(un_phi, cmap='gray')
        #plt.show()

        r=cv2.selectROI('ROI', Phi_w,False,False)
        cv2.destroyAllWindows()
        Phi_w= Phi_w[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

        #r_wx=cv2.selectROI('ROI', wx_w,False,False)
        wx_w= wx_w[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        
        
        print('Desenvolviendo ...')
        un_phi= np.unwrap(Phi_w, axis=0)
        un_phi= np.unwrap(un_phi, axis=1)
        un_wx= np.unwrap(wx_w, axis=0)
        un_wx= np.unwrap(un_wx, axis=1)

        #objeto menos el plano
        Phi_w = un_phi-un_wx

        x = np.linspace(0, Phi_w.shape[0]-1,Phi_w.shape[0])
        y = np.linspace(0, Phi_w.shape[1]-1,Phi_w.shape[1])
        print( Phi_w.shape[0]-1)
        print(Phi_w.shape[1]-1)
        xx, yy = np.meshgrid(y,x)

        #fig1 = plt.figure(figsize=(6,6))
        #a = fig1.add_subplot(projection='3d')
        #ax.set_aspect('equal')
        #ax.set_box_aspect([1,1,1])
        ax.clear()
        #ax.auto_scale_xyz(xx, yy, Phi_w)
        #ax.set_box_aspect((np.ptp(xx), np.ptp(yy), np.ptp(Phi_w)))
        ax.plot_surface(yy, xx, Phi_w,cmap=cm.YlGnBu, linewidth=0, antialiased = False )
        #ax.auto_scale_xyz([0.0, 1.0], [0.0, 1.0], [0.0, 1.0])
        #ax.set_aspect('auto')
        #plt.imshow(Phi_w,cmap='gray')
        #plt.axis('off')
        #a.set_title('Image Real')
        #ax.plot(Phi_w)
        #plt.show()
        canvas.draw()

        # Create the data.
        from numpy import pi, sin, cos, mgrid
        dphi, dtheta = pi/250.0, pi/250.0
        [phi,theta] = mgrid[0:pi+dphi*1.5:dphi,0:2*pi+dtheta*1.5:dtheta]
        m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;
        r = sin(m0*phi)**m1 + cos(m2*phi)**m3 + sin(m4*theta)**m5 + cos(m6*theta)**m7
        x = r*sin(phi)*cos(theta)
        y = r*cos(phi)
        z = r*sin(phi)*sin(theta)

        # View it.
        #from mayavi import mlab
        #s = mlab.mesh(x, y, z)
        #mlab.show()


