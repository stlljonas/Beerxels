import numpy as np 
import cv2 as cv
import math
import time
import os

## VISUALIZATION ##
def vis_circles(bigdata ,R, dim, scaling=0.1):
	# fun input would be height, width, R, color matrix, xnum/ynum can be determined form the matrix shape
	xnum = bigdata.shape[0]
	ynum = bigdata.shape[1]
	width = dim[0]
	height = dim[1]

	xcentering_value = (width - xnum*2*R-R)/2
	ycentering_value = (height - (ynum-1)*math.sqrt(3)*R - 2*R)/2
	if ycentering_value < 0	: # catching a weird edge case that probably results from rounding
		ynum = ynum-1
		ycentering_value = (height - (ynum-1)*math.sqrt(3)*R - 2*R)/2

	board = np.zeros((height,width,3), np.uint8) # creates a black image with the same dimensions as the original

	for i in range(0,xnum):
		for j in range(0,ynum):
			x_val = int(R+i*2*R + R*(j%2) + xcentering_value)
			y_val = int(R+j*math.sqrt(3)*R + ycentering_value)
			color = (bigdata[i,j,0],bigdata[i,j,1],bigdata[i,j,2])
			color = np.array((int(bigdata[i,j,0]),int(bigdata[i,j,1]),int(bigdata[i,j,2])))
			color = np.array((int(bigdata[i,j,0]),int(bigdata[i,j,1]),int(bigdata[i,j,2]))).tolist()
			#print(color)
			cv.circle(board,(x_val,y_val), R, color, -1) #	 arg1=image, arg2=center coord, ..
							# .. arg3=radius, arg4=color, arg5=thickness (negative means filled circle)
	#batcherror = batchsize - xnum*ynum

	#scaling = 0.1  
	board = cv.resize(board, (int(width*scaling),int(height*scaling)), interpolation = cv.INTER_AREA)
	
	#print(dim)
	
	'''
	print('xnum*ynum = ' + str(xnum*ynum))
	print('batcherror = ' + str(batcherror))
	print('batchsize = ' + str(batchsize))
	print('heigtherror = ' + str(height - (math.sqrt(3)*R*(ynum-1)+2*R)))
	print('widtherror = ' + str(width - (2*R*xnum+R)))
	'''
	#cv.imshow('Image',board)
	#cv.waitKey(0)
	#cv.destroyAllWindows()   
	return 0
## END VISUALIZATION ##

def vis_caps(bigdata,R,dim,cap_list,scaling = 0.1):
	xnum = bigdata.shape[0]
	ynum = bigdata.shape[1]
	width = dim[0]
	height = dim[1]	

	xcentering_value = (width - xnum*2*R-R)/2
	ycentering_value = (height - (ynum-1)*math.sqrt(3)*R - 2*R)/2
	if ycentering_value < 0	: # catching a weird edge case that probably results from rounding
		ynum = ynum-1
		ycentering_value = (height - (ynum-1)*math.sqrt(3)*R - 2*R)/2

	board = np.zeros((height,width,3), np.uint8) # creates a black image with the same dimensions as the original
	'''
	print('board dim = ' + str(height) +', ' + str(width))
	print('xnum = ' + str(xnum))
	print('ynum = ' + str(ynum))
	print('cap_list length = ' + str(len(cap_list)))
	'''
	for i in range(0,xnum):
		for j in range(0,ynum):
			x_val = int(R+i*2*R + R*(j%2) + xcentering_value)
			y_val = int(R+j*math.sqrt(3)*R + ycentering_value)

			roi = board[(y_val-R):(y_val+R+1),(x_val-R):(x_val+R+1)] # height/width are switched w.r.t x/y
			#print[i*ynum + j]
			cap_img = cap_list[i*ynum +j]
			cap_img_dim = cap_img.shape[0]
			roi_scaling = roi.shape[0]/cap_img_dim
			cap_img = cv.resize(cap_img, (roi.shape[0],roi.shape[0]), interpolation = cv.INTER_AREA)
			roi_cap = cv.add(cap_img,roi)
			board[(y_val-R):(y_val+R+1),(x_val-R):(x_val+R+1)] = roi_cap
			#cv.imshow('Image', cap_img)
			#cv.waitKey(0)
			#cv.destroyAllWindows()
			#print(cap_img_dim)

			# scale cap image to fit circle
			# copy out roi
			# create mask 
			# create inverse mask
			# black out non circle on cap (should already be the case)
			# black out circle part of roi (should also be the case)
			# add cap and roi
			# insert roi back into image



	cv.imwrite("/home/jonas/Projects/Beerxels/caps{0}.png".format(i+1),board)
	board = cv.resize(board, (int(width*scaling),int(height*scaling)), interpolation = cv.INTER_AREA)
	cv.imshow('Image',board)
	cv.waitKey(0)
	cv.destroyAllWindows()   
	return 0

