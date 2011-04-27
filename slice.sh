#!/bin/bash
# slice.sh - takes a vertical slice of specified pixel width from the middle of each
# tiff or jpeg file in current directory.  Creates slice_$1/* 
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

sliceparam=${1}x99999
if [ "x$2" == "xhoriz" ]; then
	sliceparam=99999x${1}
fi

mkdir -p slice_$1
FINDCMD='find . -maxdepth 1 -name "*.tif" -or -name "*.jpg"'
eval $FINDCMD | xargs --verbose -n 1 -P 8 -Ixxx convert xxx -gravity Center -crop ${sliceparam}+0+0 slice_$1/xxx.tif

