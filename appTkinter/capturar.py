'''
Capturar las 4 imagenes de t
 y regresar el array de cada imagen
'''

from simple_pyspin import Camera
from PIL import Image
import os

class Capturar():
    def main(self, n, t, objeto):


            with Camera() as cam: # Initialize Camera             
                
                cam.init()
                
                cam.stop()
                # Set the area of interest (AOI) to the middle half
                #cam.Width = cam.SensorWidth // 2
                #cam.Height = cam.SensorHeight // 2
                #cam.OffsetX = cam.SensorWidth // 4
                #cam.OffsetY = cam.SensorHeight // 4

                # If this is a color camera, get the image in RGB format.
                #if 'Bayer' in cam.PixelFormat:
                #    cam.PixelFormat = "RGB8"

                # To change the frame rate, we need to enable manual control
                #cam.AcquisitionFrameRateAuto = 'Off'
                #cam.AcquisitionFrameRateEnabled = True
                #cam.AcquisitionFrameRate = 15

                # To control the exposure settings, we need to turn off auto
                #cam.GainAuto = 'Off'
                # Set the gain to 20 dB or the maximum of the camera.
                #gain = min(20, cam.get_info('Gain')['max'])
                #print("Setting gain to %.1f dB" % gain)
                #cam.Gain = gain
                cam.ExposureAuto = 'Off'
                cam.ExposureTime = 10880.35
                #cam.ExposureTime = 178.87 # microseconds

                # If we want an easily viewable image, turn on gamma correction.
                # NOTE: for scientific image processing, you probably want to
                #    _disable_ gamma correction!
                #try:
                #    cam.GammaEnabled = True
                #    cam.Gamma = 2.2 #1
                #except:
                #    print("Failed to change Gamma correction (not avaiable on some cameras).")
                
                cam.start() # Start recording
                #imgs = [cam.get_array() for n in range(1)] # Get 10 frames
                imgs = cam.get_array() # Get 10 frames
                
                #cam.stop() # Stop recording

            # Make a directory to save some images
            output_dir = 'images_'+objeto
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            

            print("Saving images to: %s" % output_dir)

            # Save them
            # NOTE: images may be very dark or bright, depending on the camera lens and
            #   room conditions!
            im = Image.fromarray(imgs)
            im.save(os.path.join(output_dir, 't%d-i%d.png' % (t, n)))
            print(im)
                #cam.stop() # Stop recording
            return im