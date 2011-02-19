#!/usr/bin/python
# Interlaces slices from a timelapse series
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
import os
import sys
from multiprocessing import Pool

class SliceBlender(object):
    def __init__(self, files):
        print "Creating alpha gradient for blending slices"
        self.gradient = Image.new('L', (5*256,1))
        for x in range(512):
            self.gradient.putpixel((x, 0),x/2)
        for x in range(256):
            self.gradient.putpixel((x+2*256, 0),255)
        for x in range(512):
            self.gradient.putpixel((x+3*256, 0),255-(x/2))

        self.outdir="blended_slices"
        self.files = files
        self.image_count = len(files)
        self.width, self.height = open(files[0]).size 

    def open(self, f):
        print f,
        return Image.open(f)
    
    alphacache=dict()
    def getAlpha(self, size):
        if not self.alphacache.has_key(size[0]):
            self.alphacache[size[0]] = self.gradient.resize(size)
            
        return self.alphacache[size[0]]
    
    def splice(self, r):
        
        if not os.path.exists(self.outdir):
            print "Creating directory: %s" % self.outdir
            os.mkdir(self.outdir)

        print "Shift index %d:" % r
        output_image = Image.new('RGBA', (self.width, self.height))
    
        strips = self.image_count
    
        for i in range(strips):
            print i,
    
            offset = (r + i) % strips
            x0 = int(float(offset - 2) / strips * self.width)
            x1 = int(float(offset + 3) / strips * self.width)
            box = (x0, 0, x1, self.height)
            #print box,
        
            #im = open(files[i]).crop(box)
            im = open(self.files[(strips - 1) - abs((i * 2) - (strips - 1))]).crop(box)
        
            # resize the gradient to the size of im...
            alpha = self.getAlpha(im.size)
    
            output_image.paste(im, (x0, 0), alpha)
    
        print "Done"
        print "Saving...",
        output_image.save(self.outdir + '/combined%05d.png' % r, 'PNG')
        print "Done"


if __name__ == '__main__':
    print "Getting file list"
    files = sys.argv[1:]

    pool = Pool(processes=2)
    sliceBlender = SliceBlender(files) 
    pool.map(sliceBlender.splice, [r for r in range(len(files)) if not os.path.exists(sliceBlender.outdir + '/combined%05d.png' % r)])    
