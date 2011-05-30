#!/bin/sh

# Takes camera RAW files, creates rotated zip compressed TIFF files.
# Corrects gamma, tca and vignetting for Nikon D100 / peleng 8mm.

# IMPORTANT:  Change the fulla parameters to suit your equipment

# Bruno Postle 2006-07-20

for FILE
do
STUB=`echo $FILE | sed 's/\([[:alnum:]]\)\..*/\1/'`
if [ ! -f $STUB.tif ]; then
chmod -x $FILE
dcraw -z $FILE

# Import the RAW file
dcraw -w -4 $FILE

# Create a rotated and gamma corrected TIFF file
#convert -rotate '270' -gamma '2.2' $STUB.ppm rotate.$$.tif
convert -rotate '90' -gamma '2.2' $STUB.ppm rotate.$$.tif

# Correct TCA and vignetting
#fulla  -r 0:0:0.0005628:1.0001510 \
#       -b 0:0:-0.0002598:1.0010922 \
#       -c 1:0.198:-0.509:0.2 \
#       -i 2.2 \
#       -o tca.$$.tif \
#       rotate.$$.tif > /dev/null 2> /dev/null

# Deflate compress the TIFF file
#tiffcp -c zip tca.$$.tif zip.$$.tif
tiffcp -c zip rotate.$$.tif zip.$$.tif
mv zip.$$.tif $STUB.tif

# Create a JPEG 'proof'
convert -depth 8 $STUB.tif $STUB.jpg

# Transfer metadata lost in PPM stage
exiftool -q -q -tagsfromfile $FILE \
         -overwrite_original_in_place \
         -exif:all -author=$USER $STUB.tif $STUB.jpg
touch --reference=$FILE $STUB.tif $STUB.jpg

# Clean-up temporary files
#rm $STUB.ppm rotate.$$.tif tca.$$.tif
rm $STUB.ppm rotate.$$.tif

# Compress the RAW file, we don't need it any more
#bzip2 $FILE

echo "Created $STUB.tif $STUB.jpg `date`"
else
echo "$STUB.tif exists, skipping"
fi
done

