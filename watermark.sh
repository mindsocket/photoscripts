#!/bin/bash
mkdir -p watermarked
for f in $*; do echo $f; convert -resize 1600x1600 $f watermarked/$f; composite -gravity SouthEast ~/pics/watermark_rogerbarnesphotography_com.png watermarked/$f watermarked/$f; done
