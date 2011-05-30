#!/usr/bin/python
# image_stats.py 
#
# Output basic stats using PIL.
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
from PIL import ImageStat
import cPickle
import numpy
import os
import sys

class ImageStats(object):

    def __init__(self, files, degree=None): 
        print "getting medians"
        
        # Use the pickled stats to avoid reparsing the images
        # Delete statsPickle to recreate
        statsPickle = files[0] + "-" + str(len(files)) + ".pickle"
        if os.path.exists(statsPickle):
            print "Unpickling " + statsPickle
            self.stats = cPickle.load(open(statsPickle, 'r'))
        else:
            print "Building stats"
            self.stats = [ImageStat.Stat(Image.open(f).convert('L')) for f in files]
            cPickle.dump(self.stats, open(statsPickle, 'w'))

        self.files = files

    def printStats(self):
        for i in range(len(self.files)):
            print "File: %s Mean: %f" % (self.files[i], self.stats[i].mean[0]) 
    
if __name__ == '__main__':
    print "Getting file list"
    files = sys.argv[1:]
    
    imageStats = ImageStats(files)

    imageStats.printStats()

