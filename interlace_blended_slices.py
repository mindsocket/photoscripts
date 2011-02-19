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

from os import path
from PIL import Image
import os
import sys
import math
import subprocess
from multiprocessing import Pool

def open(f):
    print f,
    return Image.open(f)

alphacache=dict()
def getAlpha(gradient, size):
    if not alphacache.has_key(size[0]):
        alphacache[size[0]] = gradient.resize(size)
        
    return alphacache[size[0]]

def splice_func(r):
    print "Shift index %d:" % r
    output_image = Image.new('RGBA', (width, height))

    strips = image_count

    for i in range(strips):
        print i,

        offset = (r + i) % strips
        x0 = int(float(offset - 2) / strips * width)
        x1 = int(float(offset + 3) / strips * width)
        box = (x0, 0, x1, height)
        #print box,
    
        #im = open(files[i]).crop(box)
        im = open(files[(strips - 1) - abs((i * 2) - (strips - 1))]).crop(box)
    
        # resize the gradient to the size of im...
        alpha = getAlpha(gradient, im.size)

        output_image.paste(im, (x0, 0), alpha)

    print "Done"
    print "Saving...",
    output_image.save('combined%05d.png' % r, 'PNG')
    print "Done"

print "Getting file list"
files = sorted([f for f in os.listdir(path.curdir) if os.path.splitext(f)[1] == ".tif"])

print "Creating alpha gradient for blending slices"
gradient = Image.new('L', (5*256,1))
for x in range(512):
    gradient.putpixel((x, 0),x/2)
for x in range(256):
    gradient.putpixel((x+2*256, 0),255)
for x in range(512):
    gradient.putpixel((x+3*256, 0),255-(x/2))


image_count = len(files)

width, height = open(files[0]).size 

if __name__ == '__main__':
    pool = Pool(processes=2)

    pool.map(splice_func, [r for r in range(image_count) if not os.path.exists('combined%05d.png' % r)])    
