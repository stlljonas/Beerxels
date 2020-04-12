import numpy as np 
import cv2 as cv
import math
import time
import os
import sys

masterlist = []
masterlist.append([1,2])
masterlist.append([3,4,5])
print masterlist[1]
'''
directory = '/home/jonas/Projects/Beerxels/Data' # directory that contains all the images, 
masterlist = []
masterlist.append([1,2])
masterlist.append([1,2,3,4,5,6])
print masterlist

# accessing weird dimensional arrays
print masterlist[0][1]
'''
'''
for filename in os.listdir(directory):
	path = os.path.join(directory,filename)
	img = cv.imread(path)
	cv.imshow('Image',img)
	cv.waitKey(0)
	cv.destroyAllWindows()
'''
'''

for filename in os.listdir(directory):
	if filename.endswith(".jpg") or filename.endswith(".png"):
		print filename
		print os.path(filename)
		path = os.cwd()
		img = cv.imread(filename)
		cv.imshow('Image',img)
		cv.waitKey(0)
		cv.destroyAllWindows()
		print(os.path.splitext(filename)[0])
	else:
		continue
'''