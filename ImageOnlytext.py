import numpy as np
from matplotlib import colors
from scipy.spatial import cKDTree as KDTree
from scipy.misc import face
import cv2

REDUCED_COLOR_SPACE = False

# borrow a list of named colors from matplotlib
if REDUCED_COLOR_SPACE:
    use_colors = {k: colors.cnames[k] for k in ['red', 'green', 'blue', 'black' ]}
else:
    use_colors = colors.cnames

# translate hexstring to RGB tuple
named_colors = {k: tuple(map(int, (v[1:3], v[3:5], v[5:7]), 3*(16,)))
                for k, v in use_colors.items()}
ncol = len(named_colors)

"""
if REDUCED_COLOR_SPACE:
    ncol -= 1
    no_match = named_colors.pop('purple')
else:
    no_match = named_colors['purple']
"""
# make an array containing the RGB values 
color_tuples = list(named_colors.values())
#color_tuples.append(no_match)
color_tuples = np.array(color_tuples)

color_names = list(named_colors)
#color_names.append('no match')

# get example picture
img = cv2.imread('D:\\img.jpg')
img = cv2.resize(img, (150,150))
# build tree
tree = KDTree(color_tuples[:-1])
# tolerance for color match `inf` means use best match no matter how
# bad it may be
tolerance = np.inf
# find closest color in tree for each pixel in picture
dist, idx = tree.query(img, distance_upper_bound=tolerance)
# count and reattach names
counts = dict(zip(color_names, np.bincount(idx.ravel(), None, ncol+1)))
#print(colors.cnames)
print(counts)
a= list(counts.values())
elm_count = a.count(0)
print(elm_count)
