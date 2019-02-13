#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, desc
from sqlalchemy.orm import relationship

from app.models.base import _Base


class Book(_Base):
    __tablename__ = 'book'
    """
        一些属性定义重复性比较大，元类可以解决这个问题
    """
    id = Column(Integer, primary_key=True)
    number = Column(String(4), nullable=True)
    title = Column(String(20), nullable=True)
    author = Column(String(20), default='未名')
    publisher = Column(String(15))
    price = Column(Integer)
    summary = Column(String(500))
    image = Column(String(20))
    # 书籍状态（软删除）
    launched = Column(Boolean, default=False)
    # 想获得和想赠送这本书的人所有模型，列表
    _wishes = relationship('Wish', backref='book')
    _presents = relationship('Present', backref='book')

    sub_trad = relationship('Trad', backref='book')

    @property
    def wishes(self):
        if self._wishes:
            return [wish for wish in self._wishes if wish.status == 1]
        return []

    @property
    def presents(self):
        if self._presents:
            return [present for present in self._presents if present.status == 1]
        return []

    @classmethod
    def recent_books(cls, page):
        recent_books = Book.query.filter_by(
            launched=False).group_by(desc(
            Book.number)).order_by(
            Book.create_time).paginate(
            page=page, per_page=current_app.config['BOOK_LIMIT'],
            error_out=False)

        # items取得recent_books的模型列表
        recent_books = recent_books.items

        return recent_books

    # 用于快速设置参数
    def set_attrs(self, attrs_dict):
        for key, values in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, values)

    @staticmethod
    def generate_fake(count=100):
        from app.models import db
        from random import seed
        import forgery_py
        import random

        seed()
        for i in range(count):
            u = Book()
            u.number = random.randrange(1000, 9999)
            u.title = forgery_py.name.title()
            u.author = forgery_py.name.full_name()
            u.publisher = forgery_py.name.company_name()
            u.price = random.randrange(0, 101)
            u.summary = forgery_py.name.job_title()
            u.image = i + 10
            with db.auto_commit():
                db.session.add(u)
