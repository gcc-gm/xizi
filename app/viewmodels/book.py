#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 处理一本书的对象
class BookViewModel:
    def __init__(self, book):
        self.id = book.id
        self.title = book.title or ''
        self.publisher = book.publisher
        self.author = book.author
        self.price = book.price
        self.number = book.number
        self.summary = book.summary or '没有简介'
        self.image = book.image
        self.wishes = book.wishes
        self.presents = book.presents
        self.wishes_count = len(book.wishes) or 0
        self.presents_count = len(book.presents) or 0

    # 简介
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' | '.join(intros)


# 处理一推书，即书的集合
class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    # 筛选，参数some_books 为SearchBook()对象
    def fill(self, some_books, keyword=''):
        self.total = some_books.total
        self.keyword = keyword
        # 序列推到式，book
        self.books = [BookViewModel(book) for book in some_books.books]
