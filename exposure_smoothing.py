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

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageStat
import cPickle
import numpy
import os
import sys

class exposureSmoother(object):

    def __init__(self, files, degree=None): 
        print "getting medians"
        
        # Use the pickled stats to avoid reparsing the images
        # Delete statsPickle to recreate
        statsPickle = files[0] + "-" + len(files) + ".pickle"
        if os.path.exists(statsPickle):
            print "Unpickling " + statsPickle
            stats = cPickle.load(open(statsPickle, 'r'))
        else:
            print "Building stats"
            stats = [ImageStat.Stat(Image.open(f).convert('L')) for f in files]
            cPickle.dump(stats, open(statsPickle, 'w'))

        self.median = [s.median[0] for s in stats]
        if not degree:
            degree = len(self.median) / 5
        self.smoothMedian = self.smoothListGaussian(self.median, degree)
        self.ratioMedian = [x[1] / x[0] for x in zip(*[self.median , self.smoothMedian])]
        self.files = files

    def smoothFiles(self, outdir):
        if not os.path.exists(outdir):
            print "Creating directory: %s" % outdir
            os.mkdir(outdir)
        for i in range(len(self.files)):
            print "adjusting %s by %f" % (self.files[i], self.ratioMedian[i]) 
            enhancer = ImageEnhance.Brightness(Image.open(files[i]))
            newImage = enhancer.enhance(self.ratioMedian[i])
            newImage.save(outdir + '/' + self.files[i], 'TIFF')
    
    ### From: http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
    # Adapted to extend the list for processing at each end so that the smoothed list 
    # is the same length as the source list  
    def smoothListGaussian(self,lumpylist,degree=5):  
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
    
    
if __name__ == '__main__':
    print "Getting file list"
    files = sys.argv[1:]
    
    smoother = exposureSmoother(files)

    print "median:", exposureSmoother.median
    print "smoothMedian:", exposureSmoother.smoothMedian
    print "ratioMedian:", exposureSmoother.ratioMedian

    #plot(exposureSmoother.median)
    #plot(exposureSmoother.smoothMedian)

    exposureSmoother.smoothFiles("mediansmoothed")

