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

function hdr_process() {
  firstfile=$(basename $1)
  echo "Creating enfused_${firstfile}.tif..."
  align_image_stack -p ${firstfile}.pto -a aligned_${firstfile} $* && \
  enfuse -m 2048 -o enfused_${firstfile}.tif aligned_${firstfile}* 
}

if [[ $# -gt 0 ]]; then
  hdr_process $*
else
  for i in hdr_unprocessed_*; do
    echo "Processing $i directory..."
    cd $i
    hdr_process IMG_* && \
    cd .. && \
    mkdir -p hdr_processed && \
    mv $i/* hdr_processed/ && \
    rmdir $i
  done
fi
