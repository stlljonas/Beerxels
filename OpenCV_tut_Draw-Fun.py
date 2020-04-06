import cv2 as cv
import numpy as np

## [setup]
# create black image
img = np.zeros((512,512,3), np.uint8) # creates a 512x512x3 array ..
# .. for 512x512 pixels with three color values BGR each, hera all ..
# .. zeros and therefore black
## [setup]

## [draw]
# draw a diagonal blue line with thickness of 5 px
cv.line(img,(0,0),(511,511),(255,0,0),5) # arg1=image, arg2=startpx, ..
# .. arg3=endpx, arg4=color, arg5=thickness

# draw a circle
cv.circle(img,(447,63), 63, (0,0,255), -1) #	 arg1=image, arg2=center coord, ..
# .. arg3=radius, arg4=color, arg5=thickness (negative means filled circle)

# draw a rectangele
cv.rectangle(img,(384,0),(510,128),(0,255,0),3) # arg1=image, ..
# .. arg2=corner1?, arg3=corner2?, arg4=color, arg5=?

# draw an ellipse
# cv.ellipse(img,(256,256),(200,300),startAngle=0,endAngle=180,(255,0,0),-1)
# doesn't work

# draw a polygon
# coords of vertices, array of shape ROWSx1x2, where ROWS=#vertices
pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts = pts.reshape((-1,1,2))
cv.polylines(img,[pts],True, (0,255,255))

# add text
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'OpenCV',(10,500),font, 4, (255,255,255),2,cv.LINE_AA)
## [draw]

## [show_image]
cv.imshow('Image', img) # always call it 'Image', else it messes up i3
cv.waitKey(0)
cv.destroyAllWindows()	
## [show_image]


## REFERENCE: https://docs.opencv.org/3.4/dc/da5/tutorial_py_drawing_functions.html
##js-28032020
# this exercise has been brought to you by the COVID-19 Isolation
