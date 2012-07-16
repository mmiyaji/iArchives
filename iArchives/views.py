#!/usr/bin/env python
# encoding: utf-8
"""
views.py

Created by mmiyaji on 2012-07-11.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""

import sys
import os
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
def main():
    """
    """
    pass

def status404(request):
    raise Http404

if __name__ == '__main__':
    main()

