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

from PIL import Image, ImageChops
import os
from multiprocessing import Pool
import sys

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
def getAlpha(gradient, size):
    return gradient.resize(size)

def doTile(horiz, tile, files):
    #files=files[2200:2500]
    width, height = Image.open(files[0]).size 
    print "width, height:", width, height
    print "Creating alpha gradient for blending slices"
    if horiz:
        gradient = Image.new('L', (1,5*256))
        for x in range(512):
            gradient.putpixel((0, x), x/2)
        for x in range(256):
            gradient.putpixel((0, x+2*256), 255)
        for x in range(512):
            gradient.putpixel((0, x+3*256), 255-(x/2))
    else:
        gradient = Image.new('L', (5*256,1))
        for x in range(512):
            gradient.putpixel((x, 0),x/2)
        for x in range(256):
            gradient.putpixel((x+2*256, 0),255)
        for x in range(512):
            gradient.putpixel((x+3*256, 0),255-(x/2))
        
    image_count = len(files)
    outwidth = width
    outheight = height
    if horiz:
        outheight = image_count * tile
    else:
        outwidth = image_count * tile
    print "out width, height:", outwidth, outheight
    output_image = Image.new('RGBA', (outwidth, outheight))

    for i in range(image_count):
        print i, files[i]

        offset = i * tile
        
        if horiz:
            start = float(i)/image_count * height
            p0 = int(start - 2 * tile)
            p1 = int(start + 3 * tile)
            box = (0, p0, width, p1)
        else:
            start = float(i)/image_count * width
            p0 = int(start - 2 * tile)
            p1 = int(start + 3 * tile)
            box = (p0, 0, p1, height)
            
        print box
        
        try:
            im = Image.open(files[i]).crop(box)
        except IOError:
            print "brrp"
            im = Image.open(files[i - 1]).crop(box)
    
        # resize the gradient to the size of im...
        alpha = getAlpha(gradient, im.size)

        #temp_image = Image.new('RGBA', (outwidth, outheight))
        if horiz:
            #temp_image.paste(im, (0, offset))#, alpha)
            output_image.paste(im, (0, offset), alpha)
        else:
            #temp_image.paste(im, (offset, 0))#, alpha)
            output_image.paste(im, (offset, 0), alpha)

        #output_image = ImageChops.lighter(output_image, temp_image)
    print "Done"
    print "Saving...",
    output_image.save('tiled%05d.tif' % tile, 'TIFF')
    print "Done"


if __name__ == '__main__':

    index=1
    horiz = sys.argv[index] == 'horiz'
    if horiz:
        index += 1
    tile = int(sys.argv[index])         
    index += 1
    files = sys.argv[index:]
    
    doTile(horiz, tile, files)
