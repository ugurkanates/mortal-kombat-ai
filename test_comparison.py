import numpy as np
from PIL import Image,ImageChops
import math,operator
import os
cwd = os.getcwd()
fullHP = cwd+"/screens/37.png"
damageHP = cwd+"/screens/63.png"
print(cwd)
imFULL = Image.fromarray(np.asarray(Image.open(fullHP)) - np.asarray(Image.open(fullHP)))
imDAM = Image.fromarray(np.asarray(Image.open(fullHP)) - np.asarray(Image.open(damageHP)))
print(imDAM.size)
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(im1, im2)
    #diff.show()
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms
def rmsdiffe(im1, im2):
    """Calculates the root mean square error (RSME) between two images"""
    errors = np.asarray(ImageChops.difference(im1, im2)) / 255
    return math.sqrt(np.mean(np.square(errors)))
#imFULL.show()
#imDAM.show()
y = 1- rmsdiffe(imFULL,imDAM)
x= mse(np.asarray(imFULL),np.asarray(imDAM))
print("comp",y)