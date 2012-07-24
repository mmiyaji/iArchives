#!/usr/bin/env python
# encoding: utf-8
"""
upload.py

Created by mmiyaji on 2012-07-14.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from __future__ import with_statement
from views import *
import simplejson, re, urllib
from django import forms
from scan import Scanner
from django.utils.encoding import force_unicode, smart_str
from django.core import serializers
WEBSITE = 'http://ruhenheim.org/'
MIN_FILE_SIZE = 1 # bytes
MAX_FILE_SIZE = 20000000 # bytes
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES
THUMBNAIL_MODIFICATOR = '=s80' # max width / height
EXPIRATION_TIME = 300 # seconds

class UploadHandler(object):
    """
    """
    def __init__(self, request):
        """
        Arguments:
        - `request`:
        """
        self._request = request
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    def uploadGET(self):
        """
        Page to upload images.
        Case of GET REQUEST '/upload/'
        """
        temp_values = Context()
        download_script = open(os.path.join(self.BASE_DIR, 'templates/component/download_script.html')).read()
        upload_script = open(os.path.join(self.BASE_DIR, 'templates/component/upload_script.html')).read()
        temp_values = {
            "download_script":download_script,
            "upload_script":upload_script,
            }
        # logger.debug(download_script)
        return render_to_response('upload/index.html',temp_values,
                                  context_instance=RequestContext(self._request))
    def uploadPOST(self):
        """
        Page to upload images.
        Case of POST REQUEST '/upload/'
        """
        s = simplejson.dumps(self.handle_upload(), separators=(',',':'))
        if self._request.POST.has_key('redirect'):
            redirect = self._request.POST('redirect') or None
            if redirect:
                return HttpResponseRedirect(str(
                        redirect.replace('%s', urllib.quote(s, ''), 1)
                        ))
        # if 'application/json' in self._request.headers.get('Accept'):
        #     self.response.headers['Content-Type'] = 'application/json'
        # self.response.write(s)
        return HttpResponse(s, mimetype = "application/json",)
    # def initialize(self, request, response):
    #     super(UploadHandler, self).initialize(request, response)
    #     self.response.headers['Access-Control-Allow-Origin'] = '*'
    #     self.response.headers[
    #         'Access-Control-Allow-Methods'
    #         ] = 'OPTIONS, HEAD, GET, POST, PUT, DELETE'

    def validate(self, file):
        if file['size'] < MIN_FILE_SIZE:
            file['error'] = 'minFileSize'
        elif file['size'] > MAX_FILE_SIZE:
            file['error'] = 'maxFileSize'
        elif not ACCEPT_FILE_TYPES.match(file['type']):
            file['error'] = 'acceptFileTypes'
        else:
            return True
        return False

    def get_file_size(self, file):
        file.seek(0, 2) # Seek to the end of the file
        size = file.tell() # Get the position of EOF
        file.seek(0) # Reset the file position to the beginning
        return size

    def handle_upload(self):
        results = []
        blob_keys = []
        print len(self._request.POST),self._request.POST
        print self._request.FILES.getlist('files[]')
        for fieldStorage in self._request.FILES.getlist('files[]'):
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = re.sub(r'^.*\\', '',
                                    fieldStorage.name)
            result['type'] = fieldStorage.content_type
            result['size'] = self.get_file_size(fieldStorage.file)
            if self.validate(result):
                image_url = os.path.join(settings.MEDIA_URL, 'tmp', result['name'])
                destination = open(image_url, 'wb+')
                for chunk in fieldStorage.chunks():
                    destination.write(chunk)
                    destination.close()

                scan = Scanner(image_url)
                exif = scan.scanExif()
                zimage = scan.scanQR()
                published_at = None
                try:
                    if exif:
                        if exif.has_key(36867):
                            # DateTimeOriginal
                            published_at = date_validate(exif[36867], "%Y:%m:%d %H:%M:%S")
                            # datetime.datetime.strptime(exif[36867], "%Y:%m:%d %H:%M:%S")
                        elif exif.has_key(36868):
                            # DateTimeDigitized
                            published_at = date_validate(exif[36868], "%Y:%m:%d %H:%M:%S")
                            # datetime.datetime.strptime(exif[36868], "%Y:%m:%d %H:%M:%S")
                        elif exif.has_key(306):
                            # DateTime
                            published_at = date_validate(exif[306], "%Y:%m:%d %H:%M:%S")
                            # datetime.datetime.strptime(exif[306], "%Y:%m:%d %H:%M:%S")
                        else:
                            # now
                            published_at = datetime.datetime.now()
                    else:
                        published_at = datetime.datetime.now()
                except:
                    published_at = datetime.datetime.now()
                authors = []
                if zimage:
                    for i in zimage:
                        if "QRCODE" == str(i.type):
                            element = i.data.split(",")
                            print element
                            author = Author.get_by_student_id(element[2])
                            if not author:
                                author = Author()
                                author.student_id = element[2].strip()
                                author.name = element[1].strip()
                                author.nickname = element[3].strip()
                                author.save()
                            authors.append(author)
                # photo.author_id = 1
                photo = Photo.get_by_pub_and_name(published_at, result["name"])
                if photo:
                    print "Already exists?"
                    result['already'] = True
                else:
                    photo = Photo()
                photo.published_at = published_at
                photo.save(isFirst = True)
                name = force_unicode(photo.published_at.strftime((smart_str("%Y%m%d%H%M%S_"+str(photo.id).zfill(5)+"."+result['name'].split(".")[-1]))))
                photo.title = name
                photo.image = fieldStorage
                photo.original_title = result['name']
                photo.authors.clear()
                for a in authors:
                    photo.authors.add(a)
                photo.save()
                result['title'] = name
                # result['authors'] = serializers.serialize("json", photo.authors.all())
                if len(photo.authors.all()):
                    result['author'] = {'name':photo.authors.all()[0].name,
                                        'student_id':photo.authors.all()[0].student_id}
                # else:
                #     result['author'] = None
                result['published_at'] = photo.published_at.strftime("%Y-%m-%d %H:%M:%S")
                result['uuid'] = photo.uuid
                result['update_type'] = 'UPDATE'
                result['update_url'] = "http://%s/photo/%s/update/" % (self._request.get_host(), photo.uuid)
                result['delete_type'] = 'DELETE'
                result['delete_url'] = "http://%s/photo/%s/delete/" % (self._request.get_host(), photo.uuid)
                if (IMAGE_TYPES.match(result['type'])):
                    try:
                        result['url'] = "http://"+self._request.get_host()+"/media/"+photo.image.name
                        result['thumbnail_url'] = "http://"+self._request.get_host()+"/media/"+photo.thumbnail.name
                    except: # Could not get an image serving url
                        pass
                if not 'url' in result:
                    result['url'] = "http://"+self._request.get_host()+"/media/"+photo.image.name
                    result['thumbnail_url'] = "http://"+self._request.get_host()+"/media/"+photo.thumbnail.name
            results.append(result)
        return results

@csrf_protect
def home(request):
    """
    URL REQUEST '/upload/'
    """
    request_type = request.method
    # print request_type
    logger.debug(request_type)
    uhandler = UploadHandler(request)
    print request_type
    if request_type == 'GET':
        return uhandler.uploadGET()
    elif request_type == 'OPTION' or request_type == 'HEAD':
        # connection test
        return HttpResponse("OK")
    elif request_type == 'POST':
        return uhandler.uploadPOST()
    # elif request_type == 'DELETE':
    else:
        return uhandler.uploadGET()



def main():
    """
    write tests
    """
    pass

if __name__ == '__main__':
    main()

