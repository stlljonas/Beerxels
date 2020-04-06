import numpy as np 
import cv2 as cv
import math
import time


# NOTE: in cv x corresponds to width and y to height, however height has index 0 and width has 1


## PREPROCESSING ##

img = cv.imread('20200213_123528.jpg')	# import image
img = cv.medianBlur(img,3)	# blur
scaling = 0.2
width = int(img.shape[1]*scaling)
height = int(img.shape[0]*scaling)
dim = (width,height)
img = cv.resize(img, dim, interpolation = cv.INTER_AREA)


# visually check if sizing works
cv.imshow('Image',img)
cv.waitKey(0)
cv.destroyAllWindows() 

## END PREPORCESSING ##

bigbatch = 500 # how many circles are we trying to fit?   


## NEWTONS METHOD FOR SOLVING NONLINEAR EQUATION ##

def F(R,width,height): # calculate total number of circles given width, height and radius (R) and subtract the actual bigbatch nuber 
	return bigbatch - width/(2*R) + 0.5 - (width*height)/(2*math.sqrt(3)*pow(R,2)) + width/(math.sqrt(3)*R) + height/(2*math.sqrt(3)*R) - 1/math.sqrt(3)

def f(R,width,height): # calculate derivative of F
	return width/(2*pow(R,2)) + (width*height)/(math.sqrt(3)*pow(R,3)) - width/(math.sqrt(3)*pow(R,2)) - height/(2*math.sqrt(3)*pow(R,2)) 

tol = 1e-9	# tolerance for newton
maxiter = 15	# maximum iterations for Newton
error = 9999	# initialize error
k = 0	# initialize iteration counter
R_n = np.zeros(16)	# initialize R vector

R_n[0] = 0.5 * math.sqrt(width*height/bigbatch) # estimate initial guess via grid pattern of circles
#print('initial guess: R = ', R_n[0])
#print('Starting Newton Iteration')
while(error > tol and k <= maxiter):	# Newton iteration
	R_n[k+1] = R_n[k] - F(R_n[k],width,height)/f(R_n[k],width,height)
	error = np.linalg.norm(R_n[k+1]-R_n[k])		# recalculate error
	k += 1
	#print("iteration {:d}: R={:f}, error={:.15f}".format(k,R_n[k],error))
R = int(math.floor(R_n[k]))	# use result of last iteration as radius R
print('Radius: ',R)

## END NEWTON ##

# calculate 
xnum = int(math.floor((width-R)/(2*R)))
print('xnum = ', xnum)
ynum = int(math.floor((height-2*R)/(R*math.sqrt(3))+1))
print('ynum = ', ynum)   


## COLLECT DATA ##

# do I store the data in a vector or a matrix? Matrix!!

bigdata = np.zeros((xnum,ynum,3),np.uint8) # initialize matrix with saved color values (BGR)

xcentering_value = (width - xnum*2*R-R)/2
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


## VISUALIZATION ##

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
cv.imshow('Image',board)
cv.waitKey(0)
cv.destroyAllWindows()
#print(dim)
batcherror = bigbatch - xnum*ynum
print('batcherror = ', batcherror)

## END VISUALIZATION ##




