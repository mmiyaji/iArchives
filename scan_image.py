#!/usr/bin/python
from sys import argv
import zbar
import Image
import ExifTags
if len(argv) < 2: exit(1)

# create a reader
scanner = zbar.ImageScanner()

# configure the reader
scanner.parse_config('enable')

# obtain image data
image = Image.open(argv[1])
pil = image.convert('L')
width, height = pil.size
raw = pil.tostring()

exif=image._getexif()
print exif.__class__
#for tag,value in exif.items():
#    print str(tag)+ str(tag.__class__) + "==>" + str(value) + str(value.__class__)
for tag,value in exif.items():
    if tag!=37500:
        tagname=ExifTags.TAGS.get(tag)
        print str(tagname) + "==>" + str(value)
# wrap image data
image = zbar.Image(width, height, 'Y800', raw)

# scan the image for barcodes
scanner.scan(image)

# extract results
for symbol in image:
    # do something useful with results
    print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

# clean up
del(image)
