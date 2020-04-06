import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


## [read_image]
# arg1 is the path, arg2 is a flag for the way the image is read
img = cv.imread('/home/jonas/Projects/Beerxels/IMG_0614.jpg',0)
## [read_image]
cv.namedWindow('image,cv.WINDOW_NORMAL') # optional, opens Window without image
cv.waitKey(0) # optional
## [display_image]
	# displays image, arg1 = window name, arg2 = image
#cv.imshow('image',img)
	# waits arg milliseconds for keyboard input, if arg=0 it waits indefenitely
#cv.waitKey(0)
	# close all windows
#cv.destroyAllWindows()
## [display_image]
k = cv.waitKey(0)
if k == 27: # wait for ESC key to exit
	cv.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save, ord(arg) returns unicode int of character
	cv.imwrite('IMG_0614_gray.jpg', img) # saves in same directory as Script itself
	cv.destroyAllWindows()
elif k == ord('m'): # wait for 'm' key to plot with matplotlib
	plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
	plt.xticks([]), plt.yticks([]) # hide the tick values on X and Y axis
	plt.show()





#dimensions = img.shape
#print(dimensions)
#a = int(dimensions[1]/8)
# = int(dimensions[0]/8)
#print(a,b)
#imS = cv.resize(img, (a,b))     # Resize image
#cv2.imshow('image',imS)               
#cv2.waitKey()
#cv2.destroyAllWindows()w