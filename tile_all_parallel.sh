#!/bin/bash
# tile_all_parallel.sh - recursively tiles slices in batches of 100 (10 in parallel at a time)
# until there's 1 output file with all of the slices tiled. "Poor man's reduce"
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


TILE_CMD=tile.sh
PREFIX=strip
rm ${PREFIX}*

echo "tile_all stage 1"
find . -name "frame*" |sort | xargs -n 100 -P 10 ${TILE_CMD} $1
FINDCMD='find . -name "'$PREFIX'*" -type f'
IMAGE_COUNT=$(eval $FINDCMD | wc -l)
while [ $IMAGE_COUNT -gt 1 ]; do
	echo "tile_all $PREFIX"
	eval $FINDCMD |sort | xargs --verbose -n 100 -P 10 ${TILE_CMD} $1
	PREFIX=strip${PREFIX}
	FINDCMD='find . -name "'$PREFIX'*" -type f'
	IMAGE_COUNT=$(eval $FINDCMD | wc -l)
done
