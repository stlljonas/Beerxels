import numpy as np 
import cv2 as cv
import math
import time
import Pi
import Bi
import sys
import visualization
import munkres

sys.path.insert(0,'./hungarian-algorithm')
import hungarian

ref = '/home/jonas/Downloads/DSC00423.jpg'

src = '/media/jonas/ESD-USB/DCIM/100CANON' # path/to/cap/folder

limit_caps = None # a number or None for all

def color_error(color_vec1,col_vec2):
	error = np.power((color_vec1[0]-col_vec2[0]),2) + np.power((color_vec1[1]-col_vec2[1]),2) + np.power((color_vec1[2]-col_vec2[2]),2)
	return error




# call analyze_caps on folder
cap_col_vec, cap_img_list = Bi.analyze_caps(src,maxcaps=limit_caps)

	# INPUT: path to reference image, optional max number of caps to analyze (for shorter runtime while testing)
	# OUTPUT: array of Usage:

		#all the colors[G,B.R] and corresponding list of images

	# output thoughts: maybe we also need the mask for the visualization
		# note: either make it so that the filename identifies the bottlecap or create a file where we match the numbers to a picture.
		# oooooor we could just also save the image and display them in a row (maybe even with an ability to navigate), which would help a lot when assembling

# call analyze_ref on img to get matrix of colors (returns matrix)
ref_mat, R, dim = Pi.analyze_ref(ref, len(cap_col_vec))
	# input: path to image, total amount of bottlecaps
	# output: matrix of colors, radius of circles, dimensions of image

ref_dim = (ref_mat.shape[0],ref_mat.shape[1]) # (width, height)
ref_vec = ref_mat.reshape((ref_dim[0]*ref_dim[1],1,3))	# convert reference picture matrix to vector
#print('ref_mat:', ref_mat)
#print('res_vec', ref_vec)
#print(ref_dim)
'''
# testing
for i in range(0,len(cap_img_list)):
	cv.imshow('Image', cap_img_list[i])
	cv.waitKey(0)
	cv.destroyAllWindows()
# testing
'''

M = len(cap_col_vec) # number of caps
N = ref_vec.shape[0] # number of reference color values

cost_matrix = np.zeros((N,N))
#print cap_col_vec.shape
#print ref_vec.shape

# init cost matrix
for i in range(0,N):
	for j in range(0,N):
		cost_matrix[i,j] = color_error(cap_col_vec[i,:],ref_vec[j,0,:])

print('Calculating permutations...')
'''
hungarian = hungarian.Hungarian(cost_matrix)
hungarian.calculate()
res = hungarian.get_results() # returns an N long list of tuples with (cap_col,ref_col) pairings
'''
m = munkres.Munkres()
res = m.compute(cost_matrix)

print(res)

res_vec = np.zeros((ref_vec.shape[0],3))
# initialize resulting verctor

res_cap_img_list = [None] * len(res)
for i in range(0,len(res)):
	res_vec[res[i][1]] = cap_col_vec[res[i][0],:]
	res_cap_img_list[res[i][1]] = cap_img_list[res[i][0]]
	# reshuffle 

#print('R = ' + str(R))
res_mat = res_vec.reshape((ref_mat.shape[0],ref_mat.shape[1],3))
visualization.vis_caps(res_mat,R,dim,res_cap_img_list, scaling=0.5)
visualization.vis_circles(res_mat,R,dim, scaling=0.5)


# set resulting vector
# convert resulting vector to matrix



## VISUALIZATION ##


# initialinitCH

## PSEUDOCODE FITTING ALGORITHM

# initialize matrix of errors, (number of pi matrix entries X number of bi colors)
	# for each i, j in the matrix, calculate the error
	# make the matrix contain touples, so that we have the error and the coordinates


# make copy of matrix to modify
# 
# visualize 

# implement fitting algorithm
# display result with matched colors (from bi) or maybe even use the cutouts to visualize the result 

# implement some sorf of method to display and navigate the bottlecaps to help with assembly


# implement fitting algorithm 
# visualize result



## MORE STUPID IDEAS
# make a gui to adjust weightings on the actual image using the mouse