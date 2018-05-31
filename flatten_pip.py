#Author: Qin Zhang
#Date:2018/5/31
#flatten the interior of pipe
#From the bottom middle line to flatten the image from left to right
import cv2
import os
from math import pi, cos, sin
import numpy as np
import matplotlib.pyplot as plt
img = cv2.imread('flatten.png')
height, width, channel = img.shape
#choose three points
center = (int(width/2), int(height/2+40))
#define radius of two circle
out_radius = int(height-center[1]-10)
in_radius = int(out_radius/(2*2))
#get the width and height of the result rectangle image
distance_ver = out_radius - in_radius
distance_hor = int(pi*out_radius/180)
#convert image 1 degree to 1 degree, loop for 360 times
angle = 0
has_image_before = True
while angle < 2*pi:
    if angle == 0:
        top_left = [center[0],center[1]]
        bottom_left = [center[0],center[1] + out_radius]
        angle += 2*pi/360
        has_image_before = False
        continue
    top_right = top_left[:]
    bottom_right = bottom_left[:]
    top_left = [center[0] - in_radius*sin(angle),center[1]+in_radius*cos(angle)]
    bottom_left = [center[0] - out_radius*sin(angle),center[1]+out_radius*cos(angle)]
    index_before = [top_left,bottom_left,top_right,bottom_right]
    index_after = [[0,0],[0,distance_ver],[distance_hor,0],[distance_hor,distance_ver]]
    pts1 = np.float32(index_before)
    pts2 = np.float32(index_after)
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    result = cv2.warpPerspective(img,matrix,(distance_hor,distance_ver))
    if has_image_before:
        vis = np.concatenate((result, image_before), axis=1)
        #print('success concate')
        image_before = vis
    else:
        image_before = result
        has_image_before = True
    angle += 2*pi/360

#save the flattened image
cv2.imwrite('result.png',vis)
cv2.imshow('image',vis)
cv2.waitKey(0)
cv2.destroyAllWindows()
