import numpy as np
import cv2
import time
from image import *

def SlicePart(im, images, slices):
    height, width = im.shape[:2]
    sl = int(height/slices);
    directions = [1] * len(images)
    contours = [1] * len(images)
    
    # Top to bottom
    for i in range(slices):
        part = sl*i
        crop_img = im[part:part+sl, 0:width]
        images[i].image = crop_img
        images[i].Process()
        directions[i] = images[i].get_direction()
        contours[i] = images[i].getContour()
        
    return directions, contours

def RepackImages(images):
    img = images[0].image
    for i in range(len(images)):
        if i == 0:
            img = np.concatenate((img, images[1].image), axis=0)
        if i > 1:
            img = np.concatenate((img, images[i].image), axis=0)

    return img

def Center(moments):
    if moments["m00"] == 0:
        return 0

    x = int(moments["m10"]/moments["m00"])
    y = int(moments["m01"]/moments["m00"])

    return x, y

#removes white, gameboard background 
def RemoveBackground(image):
    frame = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # frame = image

    # create NumPy arrays from the boundaries
    lower = np.array([0, 0, 0], dtype = "uint8")
    # upper = np.array([100, 100, 100], dtype = "uint8")
    upper = np.array([180, 255, 80], dtype = "uint8")
    #----------------COLOR SELECTION-------------- (Remove any area that is whiter than 'upper')

    mask = cv2.inRange(frame, lower, upper)
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)
    frame = cv2.bitwise_and(frame, frame, mask = mask)
    frame = cv2.bitwise_not(frame, frame, mask = mask)
    frame = (255-frame)
    return frame


#trying to leave only a grey area (in progress)
def RemoveBW(image, b):
	low = 60
	up = 130
    # create NumPy arrays from the boundaries
	lower = np.array([low, low, low], dtype = "uint8")
	upper = np.array([up, up, up], dtype = "uint8")

	if b == True:
		mask = cv2.inRange(image, lower, upper)
		image = cv2.bitwise_and(image, image, mask = mask)
		image = cv2.bitwise_not(image, image, mask = mask)
		image = (255-image)
		return image
	else:
		return image
