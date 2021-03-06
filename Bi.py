import numpy as np 
import cv2 as cv
import math
import time
import os




## Implement for all files in a directory,
	# no return, just save data in txt or whatever


def analyze_caps(path2dir, maxcaps=None):
	# INPUT: path to reference image
	# OUTPUT: array of all the colors[G,B.R] and corresponding list of images
	
	# get  number of files
	# init
	if maxcaps == None:
		res_col_vec = np.zeros((len(os.listdir(path2dir)),3))
	else: res_col_vec = np.zeros((maxcaps,3))
	res_img_list = []

	k = 1 # loop iterator
	l = 1 # vector iterator
	for filename in os.listdir(path2dir): # iterates through all images in 
		if maxcaps != None:
			if l > maxcaps:	return res_col_vec, res_img_list;
		if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG"):
			path = os.path.join(path2dir,filename)
			res_col,res_img = analyze_cap(k,path)
			if not (res_col[0] == 0 and res_col[1] == 0 and res_col[2] == 0) :
				res_col_vec[l-1,:] = res_col
				res_img_list.append(res_img)
				l += 1
			k += 1
	return res_col_vec, res_img_list


def analyze_cap(ident,path2cap):
	print('Analyzing cap ' + str(ident) + ' ..')
	# INPUT: unique identifier, path to reference image
	# OUTPUT: array[unique identifier, average color[B,G,R], actual cutout image]
	img = cv.imread(path2cap)
	## [resize]
	scale_percent = 20 # percent of original size # should be 20
	width = int(img.shape[1]*scale_percent/100)
	height = int(img.shape[0]*scale_percent/100)
	dim = (width, height)
	img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
	## [resize]

	'''
	# testing
	cv.imshow('Image', img)
	cv.waitKey(0)
	cv.destroyAllWindows()
	'''

	# get dimensions
	dim = (height,width)
	# blur
	img = cv.medianBlur(img,3)
	# make grayscale copyt for analyses
	gimg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
				#mask = np.zeros((dim[1],dim[0],3), np.uint8)

	# apply Hough 
	# adjust minRad until only one Circle is found
	
	
	num_circles = 100
	if height < width:
		min_side = height
	else: min_side = width
	min_Rad = int(min_side/4)
	max_iterations = int(min_side/2)
	k = 0
	while(num_circles != 1):
		k += 1
		if k >= max_iterations: break	# the loop might get stuck between 0 and many circles. probably means that the image is shite
		#print(min_Rad)
		circles = cv.HoughCircles(gimg, cv.HOUGH_GRADIENT,2,20,param1=80,param2=200,minRadius=min_Rad,maxRadius=int(min_side/2))
		#print(circles)

		if min_side < 2*min_Rad or min_Rad < 10: 		# stop, if Radius has gotten too small or large
			print('No circles found in image ' + str(ident) + '!')    
			return np.array([0,0,0]),0;

		if circles is None: # we start out with a large radius and make it iteratively smaller, until we have found a single circle
			min_Rad -= 1
			continue
		circles = circles.astype(int)	# round results
		num_circles = circles.shape[1]	# how many circles were detected
		
		'''
		# testing 
		for i in circles[0,:]:
			# draw the outer circle 
			cv.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
			# draw the center of the circle 
			cv.circle(img,(i[0],i[1]),2,(0,0,255),3)
		#cv.destroyAllWindows()
		cv.imshow('Image',img)
		cv.waitKey(0)
		cv.destroyAllWindows()
		# end testing
		''' 
		if num_circles > 1:
			min_Rad += 1                   
		else: break



	# check, whether only one circle has been detected
	if circles is not None:
		if circles.shape[1] > 1:
			print('Hough Circle Detection got uncertain result')
			return np.array([0,0,0]),0;
	# get parameters of found circle
	x = circles[0,0,0]
	y = circles[0,0,1]
	rad = circles[0,0,2]
	# create region of interes (roi) around circle from color image
	roi = img[(y-rad):(y+rad+1),(x-rad):(x+rad+1)] # height/width are switched w.r.t x/y
	# create circle mask
	mask = np.zeros((2*rad+1,2*rad+1), np.uint8)
	cv.circle(mask,(rad,rad),rad,(255,255,255),-1)


	# black out non circle part of roi
 
	res = cv.bitwise_and(roi,roi, mask = mask)
	'''
	# testing
	cv.imshow('Image', res)
	cv.waitKey(0)
	cv.destroyAllWindows()
	'''
	# convert mask to binary
	bmask = cv.threshold(mask, 100,1,cv.THRESH_BINARY)
	# find num of non black px in mask
	col_px = np.sum(bmask[1][:]) # number of colored px

	# sum up values in each channel and divide by num of non black px
	#separate channels
	blue = res[:,:,0]
	green = res[:,:,1]
	red = res[:,:,2]

	# alen([name for name in os.listdir('.') if os.path.isfile(name)])verage values
	blue_av = np.sum(blue)/col_px
	green_av = np.sum(green)/col_px
	red_av = np.sum(red)/col_px
	res_col = np.zeros(3)
	res_col[0] = blue_av
	res_col[1] = green_av
	res_col[2] = red_av

	'''
	# testing 
	showres = np.zeros((512,512,3), np.uint8)
	showres[:,:] = res_col	
	cv.imshow('Image', showres)
	cv.waitKey(0)
	cv.destroyAllWindows()
	'''

	# return value
	'''
	res_arr = np.zeros(3)
	res_arr[0] = ident
	res_arr[1] = res_col	
	res_arr[2] = res
	print(type(res_arr))
	'''
	return res_col,res;

	
	

	
	
	
	
	
'''
	# testing
directory = '/home/jonas/Projects/Beerxels/Data' # directory that contains the set of beercap images

result = analyze_caps(directory)
#print result
for i in range(0,len(result)):
	cv.imshow('Image', result[i][2])
	cv.waitKey(0)
	cv.destroyAllWindows()
	showres = np.zeros((512,512,3), np.uint8)
	showres[:,:] = result[i][1]	
	cv.imshow('Image', showres)
	cv.waitKey(0)
	cv.destroyAllWindows()

print(len(result))
#for np.shape()[]
'''
