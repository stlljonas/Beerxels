import numpy as np 
import cv2 as cv

## [image_addition]
x = np.uint8([250])
y = np.uint8([10])

print(x[0],y[0])

print(cv.add(x,y)) # 250+10 = 260 => 255

print (x+y) # 250+10 = 260 % 256 = 4
## [image_addition]

## [image_blending]
# create empty images
img1 = np.zeros((512,512,3), np.uint8)
img2 = np.zeros((64,64,3), np.uint8)

# fill with color/circle
img1[:,:] = [255,255,0]
cv.circle(img2, (32,32), 30, (0,0,255), -1)
cv.imshow('Image',img1)
cv.waitKey(0)
cv.destroyAllWindows()

cv.imshow('Image',img2)
cv.waitKey(0)
cv.destroyAllWindows()

#dst = cv.addWeighted(img1,0.7,img2,1,0) # doesn't work, img1 and img2 must be same size
#.imshow('Image',dst)

## [image_blending]

## [bitwise_operation] 
# create ROI20200329_004014.jpg
# get size info
rows1,cols1,channels1 = img1.shape
rows2,cols2,channels2 = img2.shape
roi = img1[((rows1-rows2)/2):(rows1-((rows1-rows2)/2)),((cols1-cols2)/2):(cols1-((cols1-cols2)/2))]
# create a mask of circle and create it's inverse mask also
img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY) # creates grayscale circle
ret, mask = cv.threshold(img2gray,20,255,cv.THRESH_BINARY) # args: (source,maxValue,color of true,thresholdType,blockSize)
mask_inv = cv.bitwise_not(mask)

print roi.shape
print mask.shape

# black out area of circle in ROI
img1_bg = cv.bitwise_and(roi,roi, mask = mask_inv)

# take only region of circle from circle image
img2_fg = cv.bitwise_and(img2,img2, mask = mask)

# show images
cv.imshow('Image',mask)
cv.waitKey(0)
cv.destroyAllWindows()

cv.imshow('Image',img2_fg)
cv.waitKey(0)
cv.destroyAllWindows()

# put circle in roi and modify the main image  
dst = cv.add(img1_bg,img2_fg)
img1[((rows1-rows2)/2):(rows1-((rows1-rows2)/2)),((cols1-cols2)/2):(cols1-((cols1-cols2)/2))]=dst

cv.imshow('Image', img1)
cv.waitKey(0)
 


