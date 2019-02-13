#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path

DEBUG = True
BOOK_LIMIT = 20
HOST = '0.0.0.0'
PORT = 80
UPLOAD_FOLDER = path.abspath(path.dirname(__file__))+'\\static\\upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
