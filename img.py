import cv2
import numpy as np
import time

image = cv2.imread("pong.jpg", -1) #file name of image
orig = image

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #hsv format

edges = cv2.inRange(hsv, (20,0,136), (120,80,255)) #filter out unwanted colors
kernel = np.ones((5, 5), np.uint8)  #apply kernel (blurs)
edges = cv2.erode(edges, kernel) #detect edges
edges = cv2.dilate(edges, kernel)
edges = cv2.erode(edges, kernel)
edges = cv2.dilate(edges, kernel)

contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #find contours
allContours = image #stores image that has all the contours
print("Number of Contours is: " + str(len(contours)))
areas = [] #areas of contours
for contour in contours:
    ar = cv2.contourArea(contour)
    areas.append(ar)

ratio = 1 # width/height ratio
while(ratio > .5 or len(areas) == 0):
    max_area = max(areas)
    max_area_index = areas.index(max_area)  # index of the list element with largest area
    c = contours[max_area_index]
    x,y,w,h = cv2.boundingRect(c)
    fin = max(w,h)
    ratio = abs(w-h)/fin
    if(ratio > .5):
        areas.pop(max_area_index)
    
cv2.imshow('original', orig) 
cv2.waitKey(0) 

if (len(areas) > 0):
    cv2.imshow('hsv', hsv) 
    cv2.waitKey(0)
    cv2.imshow('edges', edges) 
    cv2.waitKey(0)
    cv2.rectangle(orig,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('final', orig) 
    cv2.waitKey(0)
    cv2.destroyAllWindows() 