import numpy as np 
import cv2 as cv
import math
import time
import Pi
import Bi
#from Pi import ...
#from Bi import ...
#from Bi import analyze_caps
#templ = cd.imread(None) # template that should be matched
ref = '/home/jonas/Projects/Beerxels/20200411_234519.jpg'

src = '/home/jonas/Projects/Beerxels/Data' # path/to/cap/folder


# call analyze_caps on folder
cap_data = Bi.analyze_caps(src)
	# input: src
	# output: list of touples with color and number of each bottle cap and also the corresponding cutout picture, also the total amount
	# output thoughts: maybe we also need the mask for the visualization
		# note: either make it so that the filename identifies the bottlecap or create a file where we match the numbers to a picture.
		# oooooor we could just also save the image and display them in a row (maybe even with an ability to navigate), which would help a lot when assembling

#print(cap_data)
# call analyze_ref on img to get matrix of colors (returns matrix)
ref_data = Pi.analyze_ref(ref, len(cap_data))
	# input: path to image, total amount of bottlecaps
	# output: matrix of colors 

ref_dim = (ref_data.shape[0],ref_data.shape[1])
print(ref_dim)	
## PSEUDOCODE FITTING ALGORITHM

# initialize matrix of errors, (number of pi matrix entries X number of bi colors)
	# for each i, j in the matrix, calculate the error
	# make the matrix contain touples, so that we have the error and the coordinates


# make copy of matrix to modify
# for 'number of pi entries':
	# find minimum error
	# get row and col to save as touple of pi and bi value
		# at i,j position of the pi value, set the bi value
	# set entire row and entire colum to idk, like 1000, just anything that is a lot higher than the highest error to be found
	# repeat
# visualize 

# implement fitting algorithm
# display result with matched colors (from bi) or maybe even use the cutouts to visualize the result 

# implement some sorf of method to display and navigate the bottlecaps to help with assembly


# implement fitting algorithm 
# visualize result



## MORE STUPID IDEAS
# make a gui to adjust weightings on the actual image using the mouse