#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import render_template, request

from app.models import Book
from app.viewmodels.book import BookViewModel
from app.web import web


@web.route('/')
def recent():
    page = request.args.get('page', 1, type=int)
    books_list = Book.recent_books(page)
    books = [BookViewModel(book) for book in books_list]
    return render_template('index.html', books=books)


