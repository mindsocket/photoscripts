#!/bin/bash
# slices.sh - produces 'n' roughly even vertical slices from n images in current directory
# produces files that can be fed into arrange_slices.py to interlace them
# Deprecated in favour of interlace_blended_slices.py.  This produces n^2 files on disk!
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

mkdir -p slices
FINDCMD='find . -maxdepth 1 -name "*.tif" -or -name "*.jpg"'
IMAGE_COUNT=$(eval $FINDCMD | wc -l)
eval $FINDCMD | sort | \
awk '{ print $0; print NR > "/dev/stderr" }' | \
(while read x; do [ ! -f "slices/${x}_00000.tif" ] && echo $x || echo "Skipping $x" >&2; done) | \
xargs --verbose -n 1 -P 2 -Ixxx time convert xxx -crop ${IMAGE_COUNT}x1@ slices/xxx_%05d.tif
