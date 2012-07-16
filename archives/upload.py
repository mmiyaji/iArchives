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
from django.conf import settings
from scan import Scanner
WEBSITE = 'http://ruhenheim.org/'
MIN_FILE_SIZE = 1 # bytes
MAX_FILE_SIZE = 10000000 # bytes
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
        # t = loader.get_template('component/download_script.html')
        download_script = open(os.path.join(self.BASE_DIR, 'templates/component/download_script.html')).read()
        upload_script = open(os.path.join(self.BASE_DIR, 'templates/component/upload_script.html')).read()
        # temp_values["download_script"] = download_script
        # temp_values["upload_script"] = upload_script
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
        print file
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

    def write_blob(self, data, info):
        blob = files.blobstore.create(
            mime_type=info['type'],
            _blobinfo_uploaded_filename=info['name']
            )
        with files.open(blob, 'a') as f:
            f.write(data)
        files.finalize(blob)
        return files.blobstore.get_blob_key(blob)

    def handle_upload(self):
        print "UPLOAD"
        results = []
        blob_keys = []
        print len(self._request.POST),self._request.POST
        print self._request.FILES.getlist('files[]')
        for fieldStorage in self._request.FILES.getlist('files[]'):
            print "fieldStorage:",fieldStorage,"fieldStorageTitle:",fieldStorage.file
            # form = UploadFileForm(self._request.POST, self._request.FILES)
            # print form
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = re.sub(r'^.*\\', '',
                                    fieldStorage.name)
            result['type'] = fieldStorage.content_type
            result['size'] = self.get_file_size(fieldStorage.file)
            print "name: ",result['name'], ", size: ",result['size'], ", type: ",result['type']
            if self.validate(result):
                photo = Photo(self._request.POST, fieldStorage)
                image_url = os.path.join(settings.MEDIA_URL, 'tmp', result['name'])
                destination = open(image_url, 'wb+')
                for chunk in fieldStorage.chunks():
                    destination.write(chunk)
                    destination.close()

                # blob_key = str(
                #     self.write_blob(fieldStorage.value, result)
                #     )
                # blob_keys.append(blob_key)
                scan = Scanner(image_url)
                scan.scanExif()
                blob_key = "media/tmp"
                result['delete_type'] = 'DELETE'
                result['delete_url'] = "http://"+self._request.get_host() +\
                    '/?key=' + urllib.quote(blob_key, '')
                if (IMAGE_TYPES.match(result['type'])):
                    try:
                        result['url'] = "http://"+self._request.get_host() +\
                            '/' + blob_key + '/' + urllib.quote(
                            result['name'].encode('utf-8'), '')
                        result['thumbnail_url'] = result['url']
                    except: # Could not get an image serving url
                        pass
                if not 'url' in result:
                    result['url'] = "http://"+self._request.get_host() +\
                        '/' + blob_key + '/' + urllib.quote(
                        result['name'].encode('utf-8'), '')
            results.append(result)
            print  self._request.get_host(),result['url']
            # deferred.defer(
            #     cleanup,
            #     blob_keys,
            #     _countdown=EXPIRATION_TIME
            #     )
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

