'''
Pyimagesearch Tutorial - Part Two

Last Updated: 2016-May-26
First Created: 2016-May-25

Python 2.7
Chris

http://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
http://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
http://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/
'''

import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        '''
        This algorithm is commonly known as the Ramer-Douglas-Peucker algorithm, or simply the split-and-merge algorithm.

        Contour approximation is predicated on the assumption that a curve can be approximated by a series of short line segments.

        Common values for the second parameter to cv2.approxPolyDP  are normally in the range of 1-5% of the original contour perimeter.
        '''
        # init the shape name and approximate the contour

        shape = 'unidentified'
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = 'triangle'

        # if the shape has 4, it is a square or rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approx
            # equal to one, otherwise, the shape is a rectangle

            shape = 'square' if ar >= 0.95 and ar <= 1.05 else 'rectangle'

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = 'pentagon'

        # else assume it's a circle
        else:
            shape = 'circle'

        return shape
