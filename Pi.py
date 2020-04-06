import numpy as np 
import cv2 as cv


## Implement for all files in a directory,
	# no return, just save data in txt or whatever

def getcolor(img):
	# import image
	#img = cv.imread(imgfile)

	## [resize]
	scale_percent = 20 # percent of original size # should be 20
	width = int(img.shape[1]*scale_percent/100)
	height = int(img.shape[0]*scale_percent/100)
	dim = (width, height)
	img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
	## [resize]

	cv.imshow('Image', img)
	cv.waitKey(0)
	cv.destroyAllWindows()

	# get dimensions
	dim = (height,width)
	# blur
	img = cv.medianBlur(img,3)
	# make grayscale copyt for analyses
	gimg = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
				#mask = np.zeros((dim[1],dim[0],3), np.uint8)
	# apply Hough
	circles = cv.HoughCircles(gimg, cv.HOUGH_GRADIENT,2,20,param1=80,param2=200,minRadius=50,maxRadius=400)

	# round result
	circles = circles.astype(int)
	# check, whether only one circle has been detected
	if circles.shape[1] > 1:
		print('Hough Circle Detection got uncertain result')
		#return False
	# get parameters of found circle
	x = circles[0,0,0]
	y = circles[0,0,1]
	rad = circles[0,0,2]
	# create region of interes (roi) around circle from color image
	roi = img[(y-rad):(y+rad+1),(x-rad):(x+rad+1)] # height/width are switched w.r.t x/y
	# create circle mask
	mask = np.zeros((2*rad+1,2*rad+1), np.uint8)
	cv.circle(mask,(rad,rad),rad,(255,255,255),-1)


	# testing 
	for i in circles[0,:]:	  
		# draw the outer circle 
		cv.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
		# draw the center of the circle 
		cv.circle(img,(i[0],i[1]),2,(0,0,255),3)
	cv.destroyAllWindows()
	cv.imshow('Image',img)
	cv.waitKey(0)
	cv.destroyAllWindows()


	# black out non circle part of roi
	cv.waitKey(0)
	res = cv.bitwise_and(roi,roi, mask = mask)
	# testing
	cv.imshow('Image', res)
	cv.waitKey(0)
	cv.destroyAllWindows()

	# convert mask to binary
	bmask = cv.threshold(mask, 100,1,cv.THRESH_BINARY)
	# find num of non black px in mask
	col_px = np.sum(bmask[1][:]) # number of colored px

	# sum up values in each channel and divide by num of non black px
	#separate channels
	blue = res[:,:,0]
	green = res[:,:,1]
	red = res[:,:,2]

	# average values
	blue_av = np.sum(blue)/col_px
	green_av = np.sum(green)/col_px
	red_av = np.sum(red)/col_px
	res_col = [blue_av,green_av,red_av]

	# testing 
	showres = np.zeros((512,512,3), np.uint8)
	showres[:,:] = res_col	
	cv.imshow('Image', showres)
	cv.waitKey(0)
	cv.destroyAllWindows()

	# return value
	return res_col

	
	

	
	
	
	
	