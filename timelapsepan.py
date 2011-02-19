#!/bin/python
# timelapsepan.py - crops each image in the current directory to 1920x1080,
# applying a moving crop window as it goes, saves to crop subdirectory
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

files = [f for f in os.listdir(path.curdir) if os.path.splitext(f)[1] == ".tif"]

insize = Image.open(files[0]).size
outsize = (1920, 1080)
print "insize", insize, "outsize", outsize

limit = lambda start, ins, outs: min(start, ins - outs)
startcoords = map(limit, (0, 2000), insize, outsize)
endcoords = map(limit, (2000, 100), insize, outsize)
print "start", startcoords, "end", endcoords

filecount = len(files)
step = (float(endcoords[0]) - startcoords[0]) / filecount, (float(endcoords[1]) - startcoords[1]) / filecount
print "step", step

currcoords = startcoords

outdir = os.path.join(path.curdir, "crop")
if not os.path.exists(outdir):
    os.makedirs(outdir)

for infile in files:
    print infile
    img = Image.open(os.path.join(path.curdir,infile))
    #crop
    box = map(lambda a: int(a), currcoords) + map(lambda a, b: int(a + b), currcoords, outsize)
    print box
    crop = img.crop(box)

    #save
    outfile = os.path.join(path.curdir,"crop",infile)
    crop.save(outfile + '.tif', "TIFF")

    currcoords = map(lambda x,y: x + y, currcoords, step)

