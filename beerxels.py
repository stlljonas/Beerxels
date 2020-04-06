import numpy as np 
import cv2 as cv
import math
import time
from Pi import getcolor

#templ = cd.imread(None) # template that should be matched
img = cv.imread('20200329_004014.jpg')

col = getcolor(img) # takes in the path to a file full of images and returns a list of colors, ranked after some sort of sheme, probably simple numbering
# implement fitting algorithm 
# visualize result
