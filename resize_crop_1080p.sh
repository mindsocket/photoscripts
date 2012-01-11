#!/bin/bash

for FILE
do
STUB=`echo $FILE | sed 's/\([[:alnum:]]\)\..*/\1/'`
if [ ! -f ${STUB}_cropped.jpg ]; then

convert $FILE -resize 1920x1080^ -gravity Center -extent 1920x1080 -quality 100 ${STUB}_cropped.jpg

echo "Created ${STUB}_cropped.jpg `date`"
else
echo "${STUB}_cropped.jpg exists, skipping"
fi
done

