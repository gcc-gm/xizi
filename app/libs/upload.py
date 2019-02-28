#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import request, current_app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


def filter_images(number):
    img_name = ''
    if 'img' in request.files:
        img = request.files['img']
        if img and allowed_file(img.filename):
            name, ext = os.path.splitext(img.filename)
            filename = number + ext
            try:
                img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            except Exception as e:
                raise e
            img_name = filename
    return img_name


def re_book_image(image_path):
    path = current_app.config['UPLOAD_FOLDER'] +'\\'+ image_path

    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            raise e
        return True
    return False
