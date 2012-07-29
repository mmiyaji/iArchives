#!/usr/bin/env python
# encoding: utf-8
"""
general.py

Created by mmiyaji on 2012-07-11.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

from views import *

def home(request):
    """
    Case of GET REQUEST '/'
    home page
    """
    temp_values = Context()
    temp_values = {
        "subscroll":True,
        }
    return render_to_response('general/index.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass


if __name__ == '__main__':
    main()
