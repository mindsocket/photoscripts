#!/usr/bin/python
# exposure_smoothing.py 
#
# A routine for smoothing the exposure of a set of images.
# 
# the purpose of producing an interlaced timelapse, where each frame contains
# a shifting set of slices taken from the entire range of source images
# 
# Copyright (C) 2011  Roger Barnes  http://roger.mindsocket.com.au
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from os import path
from PIL import Image
import ImageStat
import ImageEnhance
import os
import sys
import math
import subprocess
import numpy
import cPickle


def smoothFiles(files, ratioMedian, outdir):
    for i in range(len(files)):
        print "adjusting %s by %f" % (files[i], ratioMedian[i]) 
        enhancer = ImageEnhance.Brightness(Image.open(files[i]))
        newImage = enhancer.enhance(ratioMedian[i])
        newImage.save(outdir + '/' + files[i], 'TIFF')

### From: http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
# Adapted to extend the list for processing at each end so that the smoothed list 
# is the same length as the source list  
def smoothListGaussian(lumpylist,degree=5):  
    window=degree*2-1  
    weight=numpy.array([1.0]*window)  
    weightGauss=[]  
    for i in range(window):  
        i=i-degree+1  
        frac=i/float(window)  
        gauss=1/(numpy.exp((4*(frac))**2))  
        weightGauss.append(gauss)  
    weight=numpy.array(weightGauss)*weight
    listpluswindow=list([lumpylist[0]] * degree) + lumpylist + list([lumpylist[len(lumpylist)-1]] * (degree-1))
    smoothed=[0.0]*(len(listpluswindow)-window)
    for i in range(len(smoothed)):  
        smoothed[i]=sum(numpy.array(listpluswindow[i:i+window])*weight)/sum(weight)  
    return smoothed  

print "Getting file list"
files = sorted([f for f in os.listdir(path.curdir) if os.path.splitext(f)[1] == ".tif"])

# Use the pickled stats to avoid reparsing the images
# Delete statsPickle to recreate
statsPickle = "statsPickle"
if os.path.exists(statsPickle):
    print "Unpickling stats"
    stats = cPickle.load(open(statsPickle, 'r'))
else:
    print "Building stats"
    stats = [ImageStat.Stat(Image.open(f).convert('L')) for f in files]
    cPickle.dump(stats, open(statsPickle, 'w'))

print "getting medians"
median = [s.median[0] for s in stats]
degree = len(median) / 5
smoothMedian = smoothListGaussian(median, degree)
ratioMedian = [x[1] / x[0] for x in zip(*[median , smoothMedian])]

if __name__ == '__main__':

    print "median:", median
    print "smoothMedian:", smoothMedian
    print "ratioMedian:", ratioMedian

    outdir = "mediansmoothed"
    if not os.path.exists(outdir):
        print "Creating directory: %s" % outdir
        os.mkdir(outdir)
    smoothFiles(files, ratioMedian, outdir)

