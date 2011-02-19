#!/bin/bash
# tile.sh - given a list of ordered strips, this just tiles them using montage
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


# We could check the first file's dimensions to determine behaviour (horizontal or vertical tiling)
# However, the following would only work if we didn't recursively call tile with ever growing chunks 
# where the aspect ratio does not indicate intent...
#tileparam=$(identify $1 | awk '{ print $3 }' | awk -Fx '{ if ( $1 < $2 ) print "x1"; else print "1x" }')

# ...so check for an explicit parameter instead.
# Assumes vertical strips (horizontal tiling)
# this is a bit backwards, the parameter refers to the strip type, opposite to the tiling direction 
tileparam=x1
if [ "x$1" == "xhoriz" ]; then
	tileparam=1x
	shift
fi


montage $* -tile ${tileparam} -geometry +0+0 -depth 8 strip$(basename $1)

