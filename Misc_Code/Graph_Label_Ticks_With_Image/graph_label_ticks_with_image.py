'''

How to use images to label ticks on a graph.

# http://stackoverflow.com/questions/8733558/how-can-i-make-the-xtick-labels-of-a-plot-be-simple-drawings-using-matplotlib

'''

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib.image import BboxImage,imread
from matplotlib.transforms import Bbox


# define where to put symbols vertically
TICKYPOS = -.6

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range(10))

# set ticks where your images will be
ax.get_xaxis().set_ticks([2,4,6,8])
# remove tick labels
ax.get_xaxis().set_ticklabels([])


# add a series of patches to serve as tick labels
ax.add_patch(patches.Circle((2,TICKYPOS),radius=.2,
                            fill=True,clip_on=False))
ax.add_patch(patches.Circle((4,TICKYPOS),radius=.2,
                            fill=False,clip_on=False))
ax.add_patch(patches.Rectangle((6-.1,TICKYPOS-.05),.2,.2,
                               fill=True,clip_on=False))
ax.add_patch(patches.Rectangle((8-.1,TICKYPOS-.05),.2,.2,
                               fill=False,clip_on=False))

#plt.show()

lowerCorner = ax.transData.transform((.8,TICKYPOS-.2))
upperCorner = ax.transData.transform((1.2,TICKYPOS+.2))

print(lowerCorner, upperCorner)

bbox_image = BboxImage(Bbox([lowerCorner, upperCorner]),
                       norm = None,
                       origin=None,
                       clip_on=False,
                       )

bbox_image.set_data(imread('graph_label_ticks_img.png'))
ax.add_artist(bbox_image)

plt.show()

'''
bbox_image = BboxImage(Bbox([[124, 14], [146, 31]]),
                       norm = None,
                       origin=None,
                       clip_on=False,
                       )

bbox_image = BboxImage(Bbox([lowerCorner[0],
                             lowerCorner[1],
                             upperCorner[0],
                             upperCorner[1],
                             ]),
                       norm = None,
                       origin=None,
                       clip_on=False,
                       )
'''
