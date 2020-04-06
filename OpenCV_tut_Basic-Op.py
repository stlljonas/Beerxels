import cv2 as cv
import numpy as np

img = cv.imread('IMG_0614.jpg')

px = img[100,100] # get BGR values of pixel at x = 100, y = 100
print(px)

## EDITING REGIONS OF AN ARRAY
# get separate color values for pixel
blue = img[100,100,0]
green = img[100,100,1]
red = img[100,100,2]

print(blue)
print(green)
print(red)

# modify pixel
img[100,100] = [255,255,255]
print(img[100,100])


## for modifying SINGULAR PIXELS
# accessing RED value
print(img.item(10,10,2))

# modify RED value
img.itemset((10,10,2),100)
print(img.item(10,10,2))


## IMAGE PROPERTIES
# e.g. # of rows/cols, channels, # pixels, etc
print(img.shape) # returns rows, cols and channels
# greyscale only returns rows & cols

print(img.size) # returns total num px

print(img.dtype) # returns image data type
cv.namedWindow('Image')
dimensions = img.shape
print(dimensions)
a = int(dimensions[1]/8)
b = int(dimensions[0]/8)
print(a,b)
imS = cv.resize(img, (a,b))     # Resize image
cv.imshow('Image',imS)
k = cv.waitKey(0)
cv.destroyAllWindows()

## IMAGE REGION OF INTEREST (ROI)
roi = img[280:340,330:390]	# copies roi 
img[273:333,100:160] = roi 	# pastes roi to ther area

## splitting & merging image channels

b,g,r = cv.split(img) # WARNING: costly operation
print(b)
img = cv.merge((b,g,r))
b = img[:,:,0] # alternative, but equivalent result as before

img[:,:,2] = 0 # set all red pixels to 0







