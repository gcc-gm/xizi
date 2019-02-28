#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.book import Book


class SearchBook():
    def __init__(self):
        self.books = []
        self.total = 0

    def search_by_number(self, number):
        result = Book.query.filter_by(number=number).first()
        self.__fill_single(result)

    def search_by_keyword(self, keyword):
        # 得到一组Book模型{一个列表}
        result = Book.query.filter(Book.title.like("%" + keyword + "%")).all()
        self.__fill_collection(result)

    # 一本
    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    # 多本
    def __fill_collection(self, data):
        if data:
            self.total = len(data)
            self.books = data

        # 便于拿到第一本书

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
