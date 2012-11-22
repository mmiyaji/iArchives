#!/usr/bin/env python
# encoding: utf-8
"""
scan.py

Created by mmiyaji on 2012-07-16.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
import os, sys
try:
    import zbar
except:
    pass
from PIL import Image, ExifTags

class Scanner():
    """
    Scan QR tag and Exif form image.
    """
    def __init__(self, path):
        """
        load image
        Arguments:
        - `path`: image path
        """
        self.path = path
        # print "load: ",path
        # obtain image data
        self.image = Image.open(path)
        self.pil = self.image.convert('L')
        self.width, self.height = self.pil.size

    def scanExif(self):
        """
        36867	9003	DateTimeOriginal
        36868	9004	DateTimeDigitized
        306		DateTime
        """
        try:
            exif = self.image._getexif()
        except:
            exif = None
        return exif
    def scanExifAll(self):
        exif = self.scanExif()
        if exif:
            print exif.__class__
            for tag,value in exif.items():
                if tag!=37500:
                    tagname=ExifTags.TAGS.get(tag)
                    print str(tagname) + "==>" + str(value)
    def scanQR(self):
        """
        """
        raw = self.pil.tostring()
        # create a reader
        scanner = zbar.ImageScanner()

        # configure the reader
        scanner.parse_config('enable')

        # wrap image data
        zimage = zbar.Image(self.width, self.height, 'Y800', raw)

        # scan the image for barcodes
        scanner.scan(zimage)

        # extract results
        # for symbol in zimage:
        #     # do something useful with results
        #     print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        return zimage
    def get_image(self):
        return self.image
    def __def__(self):
        """
        destructor
        Arguments:
        - `self`:
        """
        # clean up
        del(self.image)

def main():
    """
    write tests
    """
    url = "./test.jpg"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    scan = Scanner(url)
    scan.scanExifAll()
    scan.scanQR()

if __name__ == '__main__':
    main()
