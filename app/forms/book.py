#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms import StringField, IntegerField, Form
from wtforms.validators import NumberRange, Length, ValidationError
from app.models.book import Book


class SearchForm(Form):
    q = StringField(validators=[Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class UploadForm(Form):
    number = StringField()
    title = StringField()
    author = StringField()
    publisher = StringField()
    price = StringField()
    summary = StringField()
    image = StringField()

    def validate_number(self, field):
        if Book.query.filter_by(number=field.data).first():
            raise ValidationError('书本已存在!')

    def validate_title(self, field):
        if Book.query.filter_by(title=field.data).first():
            raise ValidationError('书本已存在!')
