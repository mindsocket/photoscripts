#!/usr/bin/python
import sys
import math
from PIL import Image
import colorsys
import numpy as np
from itertools import izip_longest

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def hue(r,g,b):
    ''' Ganked from colorsys.rgb_to_hsv'''
    maxc = max(r, g, b) / 255.0
    minc = min(r, g, b) / 255.0
    if minc == maxc:
        return 0.0
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h

rgb_to_hue = np.vectorize(hue)

def circular_mean(angles):
    ''' Given a series of angles in radians, return the mean of circular quantities
    See: http://en.wikipedia.org/wiki/Mean_of_circular_quantities'''
    n = len(angles)
    mean = math.atan2(sum([math.sin(a) for a in angles]) / float(n), sum([math.cos(a) for a in angles]) / float(n))
    #print mean
    return mean

circular_average = lambda x, y: (x + y) / 2 if abs(x-y) < 0.5 else ((x + y - 1) / 2) % 1.0 

def hue_array(image):
	# get pixels
    arr = np.array(image.convert('RGBA').resize((200,200)))
    r, g, b, a = np.rollaxis(arr, axis=-1)
    # get hue of each
    h = rgb_to_hue(r, g, b)
#    print h.shape
#    print h[0]
	# convert from 0..1 scale to 0..2pi (radians)
    #h *= 2 * math.pi
#    print h[0]
    return h.flatten()

def reducer(l):
    pairs = l
    while len(pairs)>1:
        pairs = [circular_average(pairs[i*2],pairs[i*2+1]) for i in xrange(len(pairs)/2)]
    return pairs[0]


if __name__ == '__main__':
    #print "Getting file list"
    files = sys.argv[1:]

    #result = [(circular_mean(hue_array(Image.open(file))), file) for file in files]
    #print int((result[0][0]+math.pi)*50)
    #result = [(reduce(circular_average,sorted(hue_array(Image.open(file)))), file) for file in files]
    sorted_hue_array = lambda file: sorted(hue_array(Image.open(file)))
    result = [(reducer(sorted_hue_array(file)), file) for file in files]
    print  "%03d" % int(result[0][0]*500)
    #print sorted(result)
