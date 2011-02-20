#!/bin/bash
# timelapse.sh - encapsulates the mencoder params I'm using at the moment for HD time lapse
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

type=${1:-jpg}
mencoder "mf://*.${type}" -mf type="${type}":fps=24 -o timelapse_1080p.avi -ovc lavc -lavcopts vcodec=mpeg4:vpass=1:vbitrate=16000:autoaspect -vf scale=1920:1080
mencoder "mf://*.${type}" -mf type="${type}":fps=24 -o timelapse_1080p.avi -ovc lavc -lavcopts vcodec=mpeg4:vpass=2:vbitrate=16000:autoaspect -vf scale=1920:1080

