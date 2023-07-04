'''
Creditos GITHUB emilydeibert
'''
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from simple_pyspin import Camera
from PIL import Image
from screeninfo import get_monitors


class AcquireDisplay():
    '''Parametros globales'''
    # Actualizar frecuencia de la camara en live
    global FREQ
    FREQ = 50
    global update_freq
    update_freq = FREQ
    # Acquisición de la camra
    global running
    running = True
    # Imagen
    global image
    image = np.zeros((964, 1288))
    # Zoom
    global zoomMode
    zoomMode = False
    # Cmap
    global cmap
    cmap = 'Greys_r'

    def __init__(self, frame, can, ax, stop):
        self.m = get_monitors()
        if stop==0:
            self.stop_camera = 0
            self.frame = frame
            self.canvas = can
            self.ax = ax
        else:
            self.stop_camera = 1

    
    
    def live_camera(self):
        with Camera() as cam:  # Inicializando Camera
            


            #cam.DeviceReset()
            cam.init()
            
            # Configurar valores de la camera
            cam.Width = self.m[1].width
            cam.Height = self.m[1].height
            print('Camera dimensions: %d x %d' %(self.m[1].width, self.m[1].height))
            #cam.OffsetX = cam.SensorWidth // 4
            #cam.OffsetY = cam.SensorHeight // 4

            def _configure_trigger():
                result = True
                try:
                    # Ensure trigger mode off
                    # The trigger must be disabled in order to configure whether the source
                    # is software or hardware.
                    cam.TriggerMode = 'Off'

                    print('Trigger mode disabled...')

                    # Set TriggerSelector to FrameStart
                    # For this example, the trigger selector should be set to frame start.
                    # This is the default for most cameras.
                    cam.TriggerSelector = 'FrameStart'

                    print('Trigger selector set to frame start...')

                    # Select trigger source
                    # The trigger source must be set to hardware or software while trigger
                    # mode is off.
                    cam.TriggerSource = 'Software'

                    print('Trigger source set to software...')

                    # Turn trigger mode on
                    # Once the appropriate trigger source has been set, turn trigger mode
                    # on in order to retrieve images using the trigger.
                    cam.TriggerMode = 'On'

                    print('Trigger mode turned back on...')

                except Exception as ex:
                    print('Error: %s' % ex)
                    return False

                return result
            
            

            # Cambiar el frame rate
            cam.AcquisitionFrameRateAuto = 'Off'
            cam.AcquisitionFrameRateEnabled = True
            cam.AcquisitionFrameRate = 8

            cam.AcquisitionMode = 'Continuous'
            cam.ExposureAuto = 'Off'
            cam.ExposureTime = 24880.35
            try:
                cam.GammaEnabled = True
                cam.Gamma = 2.2
            except Exception as e:
                print(e)

            def _zoomOut():
                global zoomMode
                zoomMode = False

            def _zoomIn():
                global zoomMode
                zoomMode = True

            

            def _grab_next_image_by_trigger():
                try:
                    result = True
                    # Use trigger to capture image
                    # The software trigger only feigns being executed by the Enter key;
                    # what might not be immediately apparent is that there is not a
                    # continuous stream of images being captured; in other examples that
                    # acquire images, the camera captures a continuous stream of images.
                    # When an image is retrieved, it is plucked from the stream.
                    # Execute software trigger
                    cam.TriggerSoftware()
                    print('execccute')

                except Exception as ex:
                    print('Error: %s' % ex)
                    return False

                return result
             # Funcines

            def _acquire_images():
                    # Configurar Trigger
                if _configure_trigger() is False:
                    return False
                try:
                    result = True
                    print('Acquiring images...')

                    # Retrieve, convert, and save images
                    #  Retrieve the next image from the trigger
                    result &= _grab_next_image_by_trigger()
                    image_result = cam.get_array(wait=True)

                    # Ensure image completion
                    #if image_result.IsInComplete():
                    #    print('Image incomplete with image status %d ...' %
                    #          image_result.GetImageStatus())
                    #else:
                    filename = 'Trigger-holi.png'
                    image_result.Save(filename)
                    print('Image saved at %s\n' % filename)
                        #  Release image
                        #
                        #  *** NOTES ***
                        #  Images retrieved directly from the camera (i.e. non-converted
                        #  images) need to be released in order to keep from filling the
                        #  buffer.
                    image_result.Release()
                except Exception as ex:
                    print('Error: %s' % ex)
                    return False

                _reset_trigger()
                return result
            
            def _reset_trigger():
                #This function returns the camera to a normal state by turning off trigger mode.
                try:
                    result = True
                    cam.TriggerMode = 'Off'
                    
                    print('Trigger mode disabled...')
                except Exception as ex:
                    print('Error: %s' % ex)
                    result = False

                return result
            
            def _update():
                try:
                    if running:
                        if self.stop_camera == 1:
                            cam.stop()
                            print('Deteniendose ...')
                            return 0
                        global image
                        image = cam.get_array()
                        if zoomMode:
                            image = image[422:542, 563:724]
                        im.set_data(image)
                        im.set_cmap(cmap)
                        self.canvas.draw()
                        self.frame.after(update_freq, _update)

                except Exception as e:
                    print(e)
            #def _cam_stop():
            #    cam.stop()

            
            # Bottom zoom IN
            #btt_in = tk.Button(self.frame,  text='Stop', command= _cam_stop)
            #btt_in.pack(side=tk.TOP, padx=1, pady=1)
            # Comenzar camara
            cam.start()
            # Configurar Trigger
            #print(cam.document())

            # Crear figura para agregar el canvas
            #fig = Figure(figsize=(5, 5),  dpi=100)
            #ax = fig.add_subplot()
            #ax.set_yticks([])
            #ax.set_xticks([])

            #global imag
            image = cam.get_array()
            im = self.ax.imshow(image, vmin=0, vmax=255, cmap=cmap)

            # Crear canvas para dibujar la imagen de la camara
            #canvas = FigureCanvasTkAgg(fig, master=self.frame)
            #bbox = canvas.bbox(tk.ALL)
            #canvas.config(width=bbox[2] - bbox[0])
            #canvas.draw()
            #canvas.get_tk_widget().grid(row=0, column=0)
            #canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            global running
            running = True

            val = cam.ExposureTime
            print('ExposureTime: ', val)
            # cam.ExposureTime = val # we force set an exposure time. If not, the update may be buggy
            # cam.ExposureTime = 10000 # we force set an exposure time. If not, the update may be buggy

            if running:
                #cam.AcquisitionMode = 'Continuous'
                global update_freq
                update_freq = FREQ
                _update()  # updates the image every 5 milliseconds

            # Bottom zoom IN
            #btt_in = tk.Button(self.frame,  text='Trigger', command= _acquire_images)
            #btt_in.pack(side=tk.TOP, padx=1, pady=1)

            # Bottom zoom OUT
            #btt_out = tk.Button(self.frame, text='Alejar', command=_zoomOut)
            #btt_out.grid(row=2, column=2)

            #tk.mainloop()
            cam.stop()
            # self.frame.quit()     # stops mainloop
