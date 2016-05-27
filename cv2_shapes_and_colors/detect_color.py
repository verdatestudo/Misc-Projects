'''
Pyimagesearch Tutorial - Part Three

Last Updated: 2016-May-26
First Created: 2016-May-25

Python 2.7
Chris

http://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
http://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
http://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/

'''

from shapedetector import ShapeDetector
from colorlabeler import ColorLabeler
import imutils
import cv2

# load the image and resize it to a smaller factor
# so that the shapes can be approximated better

my_image = 'shapes_and_colors.jpg'

image = cv2.imread(my_image)
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# blur the resized image slightly, then convert it to both
# graysale and the L*a*b* color spaces

blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# init
sd = ShapeDetector()
cl = ColorLabeler()

# loop over cnts

for c in cnts:

    # compute the center of the contour

    M = cv2.moments(c)
    try:
        cX = int((M['m10'] / M['m00']) * ratio)
        cY = int((M['m01'] / M['m00']) * ratio)
    except:
        cX = 0
        cY = 0

    # detect the shape of the contour and label the color

    shape = sd.detect(c)
    color = cl.label(lab, c)

    # multiply the contour (x, y) coords by the resize ratio,
    # then draw the contours and the name of the shape and labeled
    # color on the image

    c = c.astype('float')
    c *= ratio
    c = c.astype('int')
    text = '{} {}'.format(color, shape)
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# show image

cv2.imshow('image', image)
cv2.waitKey(0)
