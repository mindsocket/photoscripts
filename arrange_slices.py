#!/usr/bin/python
# arrange_slices.py
#
# Processes a directory full of sliced up images into a series of interlaced ones for
# the purpose of producing an interlaced timelapse, where each frame contains
# a shifting set of slices taken from the entire range of source images
# 
# No longer under development, interlace_blended_slices.py does the slicing and interlacing in one
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
import os
import sys
import math
import subprocess

print "Getting file list"
files = sorted([f for f in os.listdir(path.curdir) if os.path.splitext(f)[1] == ".tif"])

file_count = len(files)
frame_count = math.sqrt(file_count)
print "Frame count: %d" % frame_count

# We should have a square number of files, bail if we don't
if frame_count != int(frame_count):
    print "Exiting"
    sys.exit()

args = dict()    

frame_count = int(frame_count)
for frame in range(frame_count):
    outdir = os.path.join(path.curdir, "frame%05d" % frame)
    args[frame] = dict()
    if not os.path.exists(outdir):
        print "Creating directory: %s" % outdir
        os.mkdir(outdir)

output_offset_counter = -1
slice_counter = 0

for infile in files:
    if slice_counter % frame_count == 0:
        output_offset_counter += 1
        print "Cycle %d/%d" % (output_offset_counter, frame_count)
    #if ((output_offset_counter + slice_counter) % frame_count) == 0:
    frame_number = (output_offset_counter + slice_counter) % frame_count
    #print "%d/%d: Linking %s to frame%05d/frame%05d.tif" % (slice_counter, file_count, infile, frame_number, slice_counter % frame_count)
    #subprocess.check_call(['ln', '-s', '../' + infile, "frame%05d/frame%05d.tif" % (frame_number, slice_counter % frame_count)])
    args[frame_number][slice_counter % frame_count] = infile
    #print args
    slice_counter += 1

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        
for frame in range(frame_count)[30:]:
    call_list = [args[frame][key] for key in sorted(args[frame].iterkeys())]
    print "%d/%d: Generating image %s ... %s" % (frame, frame_count, call_list[0], call_list[frame_count - 1])

    processes = list()
    combine=list(['tile.sh'])
    for chunk in chunks(call_list, 101):
        print "running chunk for %s" % chunk[0]
        pathchunk = [os.path.join(path.abspath(path.curdir), f) for f in chunk]
        pathchunk.insert(0, 'tile.sh')
        processes.append(subprocess.Popen(pathchunk, cwd="/dev/shm"))
        combine.append('/dev/shm/strip'+chunk[0])

    for p in processes:
        p.wait()

    print "running combine"
    combine_process = subprocess.Popen(combine, cwd="../combined")
    combine_process.wait()
    subprocess.call(['find', '/dev/shm', '-name', 'strip*', '-delete'])
