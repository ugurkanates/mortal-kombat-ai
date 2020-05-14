from PIL import Image,ImageChops
import numpy as np
import math,operator
import os
path = os.getcwd()
print(path)
timer = (181, 6, 208, 25) # thanks ImageMagics for pixel coordinates
P1_health_box = (20,30,182,40)
P2_health_box = (207,30,368,40)
crop_timer_img = (Image.open(path+"/assets/timer.png"))
crop_timer_img = crop_timer_img.convert("RGB")
# from single image returns PIL type cropped timer for comparison
# if fight started etc

def crop_timer(imge):
    imge = Image.fromarray(imge,mode="RGB")
    imge = imge.crop(timer)
    return imge

# its a very naive approach but I found it's working so why not
# anything else would be improement , histogram based ones etc 
# or teaching OCR network like tesseract for mame fonts
# but didn't have time for it so its basic pixel comparison cheers :D
# returns their difference so 1- output will be how similiar they are.

def rmsdiffe(im1, im2):
    """Calculates the root mean square error (RSME) between two images"""
    #print(im1 , im2)
    errors = np.asarray(ImageChops.difference(im1, im2)) / 255
    return math.sqrt(np.mean(np.square(errors)))