#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship, backref

from app.models import User
from app.models.base import _Base


class Wish(_Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    launched = Column(SmallInteger, default=1)
    # 还有一个来自book反向引用的属性 book #
    # 还有一个来自user反向引用的属性 owner #

    # 模型关联 得到列表
    # trad_info = relationship('Trad', backref=backref('wish'))

    def is_yourself_wishes(self, uid):
        user = User.query.get(uid)
        if self.owner == user:
            return False
        return True

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        from app.models.user import User
        from app.models import db, Book

        seed()
        user_count = User.query.count()
        book_count = Book.query.count()
        for i in range(count):
            book = Book.query.offset(randint(0, book_count - 1)).first()
            owner = User.query.offset(randint(0, user_count - 1)).first()
            w = Wish()
            w.book = book
            w.owner = owner
            with db.auto_commit():
                db.session.add(w)
