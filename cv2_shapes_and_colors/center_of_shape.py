'''
Pyimagesearch Tutorial - Part One

Last Updated: 2016-May-26
First Created: 2016-May-25

Python 2.7
Chris

http://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
http://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
http://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/
'''

import imutils
import cv2


# load the image, convert to grayscale, blur it slightly and threshold it.

my_image = 'shapes_and_colors.jpg'

image = cv2.imread(my_image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# show picture

cv2.imshow('image', thresh)
cv2.waitKey(0) #waits specified time for key press, can also specify which key

# find contours in the threshold image
# cnts[0] if opencv2.4, cnts[1] if opencv3

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours

for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    try:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
    except: # some M results = 0, just move on
        cX = 0
        cY = 0

    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, 'center', (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# show the image
cv2.imshow('image', image)
cv2.waitKey(0) #waits specified time for key press, can also specify which key
