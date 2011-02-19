#!/bin/bash
# pano_process.sh - run autopano-sift-c across pano_unprocessed/* and move the results
# to pano_processed
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

cd pano_unprocessed
firstfile=$(ls IMG_* | head -n 1)
autopano-sift-c ${firstfile}.pto IMG_*
#autooptimiser ${firstfile}.pto -o ${firstfile}.pto
cd -
mkdir -p pano_processed
mv pano_unprocessed/* pano_processed/

