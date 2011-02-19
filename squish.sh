#!/bin/bash
# squish.sh - run this on thick slices (eg "tile.sh 64" output) to make thin slices (eg "squish.sh 4")
# similar to just running tile, but squishes more information into each slice.
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

mkdir squish_$1
#for i in *.jpg; do echo $i; convert $i -resize ${1}x720\! squish_$1/$i; done
find . -maxdepth 1 -name "*.tif" | xargs --verbose -n 1 -P 8 -Ixxx convert xxx -resize ${1}x720\! squish_$1/xxx
