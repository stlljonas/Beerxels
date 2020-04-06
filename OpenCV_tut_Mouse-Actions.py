import cv2 as cv
import numpy as np

# list all available mouse events

events = [i for i in dir(cv) if 'EVENT' in i]
print(events)
cv.namedWindow('Image')
k = cv.waitKey(0)

## [simple]
if k == ord('s'): # press 's' for simple circles
	# mouse callback function
	def draw_circle(event,x,y,flags, param):
		print('draw_circle called \n')
		if event == cv.EVENT_LBUTTONDBLCLK:
			cv.circle(img,(x,y), 100, (255,0,0),-1)

	# create a black image, a window and bind the function to window
	img = np.zeros((512,512,3), np.uint8)
	#cv.namedWindow('Image')
	cv.setMouseCallback('Image', draw_circle)
	print('passed setMouseCallback \n')


	## [ESC_to_exit_Implementation]
	while(1):
		cv.imshow('Image', img)
		if cv.waitKey(20) & 0xFF == 27: # 0xFF = 255 = 000000..0011111111, which ..
	# .. combined with the AND operation only leaves the last 8 bits. 27 = Esc in unicode
			break
	cv.destroyAllWindows()
	## [ESC_to_exit_Implementation]
## [simple]

## [advanced]
if k == ord('a'): # press a for advanced circles
 	drawing = False # true if mouse is pressed
	mode = True # if True, draw rectangle. Press 'm' to toggle to curve
	ix,iy = -1,-1
	print('draw_circle_a')
	# mouse callback function
	def draw_circle_a(event,x,y,flags,param):
		global ix,iy, drawing, mode

		if event == cv.EVENT_LBUTTONDOWN: # when we press the button, we are drawing and setting our point 0
			drawing = True
			ix,iy = x,y

		elif event == cv.EVENT_MOUSEMOVE: # when the mouse moves ..
			if drawing == True:			  # .. and we are drawing ..
				if mode == True:
					cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1) # we draw a rectangle ..
				else:			
					cv.circle(img,(x,y),5,(0,0,255),-1)		# .. or circles, depending on the mode

		elif event == cv.EVENT_LBUTTONUP: # when we lift the button .. 
			drawing = False 		# .. we are no longer drawing
			if mode == True:		# drawing one last circle/rectangle, is not necessary
				cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
			else:
				cv.circle(img,(x,y),5,(0,0,255),-1)
	# end fun
	img = np.zeros((512,512,3),np.uint8)	# create blank image
	#cv.namedWindow('Image')
	cv.setMouseCallback('Image', draw_circle_a)
	i = 0 # keep track of loops
	while(1):
		i += 1
		print(i)
		cv.imshow('Image',img)
		k = cv.waitKey(1) & 0xFF
		if k == ord('m'):
			mode = not mode
		elif k == 27:
			break
## [advanced]
cv.destroyAllWindows()
