#!/bin/bash
# hdr_process.sh - go through hdr_unprocessed_*/IMG_* and produce aligned and enfused
# images for each directory in hdr_processed/
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

for i in hdr_unprocessed_*; do
  cd $i
  firstfile=$(ls IMG_* | head -n 1)
  align_image_stack -p ${firstfile}.pto -a aligned_${firstfile} IMG_*
  enfuse -o enfused_${firstfile}.tif aligned_${firstfile}*
  cd ..
  mkdir -p hdr_processed
  mv $i/* hdr_processed/
  rmdir $i
done

