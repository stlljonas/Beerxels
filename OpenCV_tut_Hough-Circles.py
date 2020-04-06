import numpy as np 
import cv2 as cv

img = cv.imread('20200329_004014.jpg',0)

## [resize]
scale_percent = 20 # percent of original size
width = int(img.shape[1]*scale_percent/100)
height = int(img.shape[0]*scale_percent/100)
dim = (width, height)
#cv.imshow('Image',img)
#cv.waitKey(0)
img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
## [resize]

## [blur]
#cv.destroyAllWindows()
img = cv.medianBlur(img,3)
#cv.imshow('Image',img)
#cv.waitKey(0)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
print('before')
## [blur]

## [Hough]
circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT,2,20,param1=80,param2=200,minRadius=50,maxRadius=400)
circles = circles.astype(int)
print(circles)
for i in circles[0,:]:	  
	# draw the outer circle 
	cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
	# draw the center of the circle 
	cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv.destroyAllWindows()
cv.imshow('Image',cimg)
cv.waitKey(0)
cv.destroyAllWindows()