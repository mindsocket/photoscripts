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
from multiprocessing import Pool
import sys

def openImage(f):
    print f,
    return Image.open(f)

class memoize:
    # from http://avinashv.net/2008/04/python-decorators-syntactic-sugar/
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]

@memoize
def getAlpha(size):
    return gradient.resize(size)

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
        print box,
    
        #im = openImage(files[i]).crop(box)
        im = openImage(files[(strips - 1) - abs((i * 2) - (strips - 1))]).crop(box)
        #im = openImage(files[image_count * ((strips - 1) - abs((i * 2) - (strips - 1))) / strips]).crop(box)
    
        # resize the gradient to the size of im...
        alpha = getAlpha(im.size)

        output_image.paste(im, (x0, 0), alpha)

    print "Done"
    print "Saving...",
    output_image.save('blended_slices/combined%05d.png' % r, 'PNG')
    print "Done"

print "Creating alpha gradient for blending slices"
gradient = Image.new('L', (5*256,1))
for x in range(512):
    gradient.putpixel((x, 0),x/2)
for x in range(256):
    gradient.putpixel((x+2*256, 0),255)
for x in range(512):
    gradient.putpixel((x+3*256, 0),255-(x/2))

files = sorted([f for f in os.listdir(os.path.curdir) if os.path.splitext(f)[1] == ".tif"])
image_count = len(files)

width, height = openImage(files[0]).size 

if __name__ == '__main__':

    files = sys.argv[1:]
    image_count = len(files)
    
    width, height = openImage(files[0]).size 

    pool = Pool(processes=2)
    pool.map(splice_func, [r for r in range(image_count) if not os.path.exists('blended_slices/combined%05d.png' % r)])    
