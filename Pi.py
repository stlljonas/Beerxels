import numpy as np 
import cv2 as cv
import math
import time
import os

# NOTE: in cv x corresponds to width and y to height, however height has index 0 and width has 1


def F(R,width,height, batchsize): # calculate total number of circles given width, height and radius (R) and subtract the actual bigbatch nuber 
		return batchsize - width/(2*R) + 0.5 - (width*height)/(2*math.sqrt(3)*pow(R,2)) + width/(math.sqrt(3)*R) + height/(2*math.sqrt(3)*R) - 1/math.sqrt(3)

def f(R,width,height, batchsize): # calculate derivative of F
		return width/(2*pow(R,2)) + (width*height)/(math.sqrt(3)*pow(R,3)) - width/(math.sqrt(3)*pow(R,2)) - height/(2*math.sqrt(3)*pow(R,2)) 

def analyze_ref(picpath, batchsize):
	# INPUT: path to picture
	# OUTPUT: matrix of colors
	## PREPROCESSING ##
	print('Analyzing reference..')
	img = cv.imread(picpath)

	img = cv.medianBlur(img,3)	# blur
	scaling = 1
	width = int(img.shape[1]*scaling)
	##print('width = ' + str(width))
	height = int(img.shape[0]*scaling)
	##print('height = ' + str(height))
	dim = (width,height)
	img = cv.resize(img, dim, interpolation = cv.INTER_AREA)

	'''
	# visually check if sizing works
	cv.imshow('Image',img)
	cv.waitKey(0)
	cv.destroyAllWindows() 
	'''
	## END PREPORCESSING ##


	## NEWTONS METHOD FOR SOLVING NONLINEAR EQUATION ##

	
	tol = 1e-9	# tolerance for newton
	maxiter = 15	# maximum iterations for Newton
	error = 9999	# initialize error
	k = 0	# initialize iteration counter
	R_n = np.zeros(16)	# initialize R vector

	R_n[0] = 0.5 * math.sqrt(width*height/batchsize) # estimate initial guess via grid pattern of circles
	#print('initial guess: R = ', R_n[0])
	#print('Starting Newton Iteration')
	while(error > tol and k < maxiter):	# Newton iteration
		R_n[k+1] = R_n[k] - F(R_n[k],width,height,batchsize)/f(R_n[k],width,height,batchsize)
		# alternative error: 
		k += 1
		error = np.linalg.norm(R_n[k]-R_n[k-1])		# recalculate error

		#print("iteration {:d}: R={:f}, error={:.15f}".format(k,R_n[k],error))
	
	## END NEWTON ##
	R = int(math.floor(R_n[k]))	# use result of last iteration as radius R
	# find best rounding to maximize used caps while not exceeding the batchsize
	xnum_ex = (width-R_n[k])/(2*R_n[k])
	ynum_ex = (height-2*R_n[k])/(R_n[k]*math.sqrt(3))+1
	##print('xnum_ex, ynum_ex = ' + str(xnum_ex) + ', ' + str(ynum_ex))
	'''
	xnum_ceil = int(math.ceil((width-R)/(2*R)))
	xnum_floor = int(math.floor((width-R)/(2*R)))
	ynum_ceil = int(math.ceil((height-2*R)/(R*math.sqrt(3))+1))
	ynum_floor = int(math.floor((height-2*R)/(R*math.sqrt(3))+1))
	'''
	xnum_ceil = int(math.ceil(xnum_ex))
	xnum_floor = int(math.floor(xnum_ex))
	ynum_ceil = int(math.ceil(ynum_ex))
	ynum_floor = int(math.floor(ynum_ex))

	#print('xnum_ceil = ' + str(xnum_ceil) + '; xnum_floor = ' + str(xnum_floor) + '; ynum_ceil = ' + str(ynum_ceil) + '; ynum_floor = ' + str(ynum_floor))
	'''
	if (batchsize - xnum_ceil*ynum_ceil) >= 0: 
		xnum = xnum_ceil
		ynum = ynum_ceil
	elif (batchsize - xnum_ceil*ynum_floor) > 0 and xnum_ceil*ynum_floor > xnum_floor*ynum_ceil: 
		xnum = xnum_ceil        
		ynum = ynum_floor
	elif (batchsize - xnum_floor*ynum_ceil) >= 0:
		xnum = xnum_floor 
		ynum = ynum_ceil
	elif (batchsize - xnum_floor*ynum_floor) >= 0:
		xnum = xnum_floor
		ynum = ynum_floor
	else:
		xnum = xnum_floor 	# eliminate the possibility of using mor botttle caps than we actually have
		ynum = ynum_floor-1
		 '''
	xnum = xnum_floor
	ynum = ynum_floor	 
	#print('xnum, ynum = ' + str(xnum) + ', ' + str(ynum))
	'''
	xnum = int(math.floor((width-R_n[k])/(2*R_n[k])))
	ynum = int(math.floor((height-2*R_n[k])/(R_n[k]*math.sqrt(3))+1))	
	'''
	
	#print('Radius: ' + str(R))


	## COLLECT DATA ##

	# do I store the data in a vector or a matrix? Matrix!!

	bigdata = np.zeros((xnum,ynum,3),np.uint8) # initialize matrix with saved color values (BGR)

	xcentering_value = (width - xnum*2*R-R)/2
	ycentering_value = (height - (ynum-1)*math.sqrt(3)*R - 2*R)/2
	if ycentering_value < 0	: # catching a weird edge case that probably results from rounding
		ynum = ynum-1
		ycentering_value = (height - (ynum-1)*math.sqrt(3)*R - 2*R)/2

	#print('xcentering_value = ',xcentering_value,'ycentering_value =', ycentering_value)
	for i in range(0,xnum):
		for j in range(0,ynum):
			# calculate x and y pos of current circle
			#print('i: ', i, '; j: ', j)
			x_val = int(R+i*2*R + R*(j%2)+ xcentering_value)
			y_val = int(R+j*math.sqrt(3)*R + ycentering_value)
			#print('x_val = ',x_val,'   y_val = ',y_val)
			# create region of interes (roi) around circle from color image
			roi = img[(y_val-R):(y_val+R+1),(x_val-R):(x_val+R+1)] # height/width are switched w.r.t x/y
			#print('roi: ',roi.shape)
			# create circle mask
			mask = np.zeros((2*R+1,2*R+1), np.uint8)
			#print('mask: ',mask.shape)
			cv.circle(mask,(R,R),R,(255,255,255),-1)
	 		# black out non circle part of roi
			res = cv.bitwise_and(roi,roi, mask = mask)
			# convert mask to binary
			bmask = cv.threshold(mask, 100,1,cv.THRESH_BINARY)
			# find num of non black px in mask
			col_px = np.sum(bmask[1][:]) # number of colored (non-black) px
			
			# sum up values in each channel and divide by num of non black px
			# separate channels
			blue = res[:,:,0]
			green = res[:,:,1]
			red = res[:,:,2]

			# average values
			blue_av = np.sum(blue)/col_px
			green_av = np.sum(green)/col_px
			red_av = np.sum(red)/col_px
			res_col = [blue_av,green_av,red_av] # recombine color channels

			bigdata[i,j,:] = res_col # save color to matrix

	## END COLLECT DATDA ##
	return bigdata, R, dim 




'''
picpath = '/home/jonas/Downloads/20200222_013257.jpg'

batchsize = 180  
bigdata, R, dim = analyze_ref(picpath,batchsize)
visualize_circles(bigdata,R,dim)
'''
'''
for i in range(0,50) :      
	batchsize = 400+i
	analyze_ref(picpath,batchsize)
#batchsize = 200 # how many circles are we trying to fit?   
'''



 