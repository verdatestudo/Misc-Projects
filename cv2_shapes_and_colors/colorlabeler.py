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

from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init__(self):

        '''
        Finally, we convert the NumPy 'image' from the RGB color space to the L*a*b* color space.
        So why are we using the L*a*b* color space rather than RGB or HSV?
        Well, in order to actually label and tag regions of an image as containing a certain color,
        we'll be computing the Euclidean distance between our dataset of known colors
        (the lab array) and the averages of a particular image region.
        '''

        # init the colors dict, containing the color name and RGB value
        colors = OrderedDict({'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'yellow': (220, 180, 70), 'orange': (255, 160, 50)})

        # allocate memory for the L*a*b* image, then init the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype='uint8')
        self.colorNames = []

        # loop over the colors dict
        for (i, (name, rgb)) in enumerate(colors.items()):
            # update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)

        # convert the L*a*b* array from the RGB color space to L*a*b*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):
        '''
        Figure 1: (Right) The original image. (Left) The mask image for the blue pentagon at the bottom of the image,
        indicating that we will only perform computations in the 'white' region of the image, ignoring the black background.

        Notice how the foreground region of the mask is set to white, while the background is set to black.
        We'll only perform computations within the masked (white) region of the image.

        We also erode the mask slightly to ensure statistics are only being computed for the masked region and that no background
        is accidentally included (due to a non-perfect segmentation of the shape from the original image, for instance).
        '''

        # construct a mask for the contour, then compute the
        # average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype='uint8')
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]

        # init the min distance found thus far
        minDist = (np.inf, None)

        # loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current L*a*b*
            # color value and the mean of the image
            d = dist.euclidean(row[0], mean)

            # if the distance is smaller than the current distance
            # then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, i)

        # return the name of the color with the smallest distance
        return self.colorNames[minDist[1]]
