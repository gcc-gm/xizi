#!/usr/bin/env python
# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, ForeignKey, SmallInteger

from app.models import User
from app.models.base import _Base


class Present(_Base):
    __tablename__ = 'present'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    launched = Column(SmallInteger, default=1)
    # 还有一个 book 的来自book反向引用的属性 #
    # 还有一个 user 的来自user反向引用的属性 #

    # 模型关联
    # trad_info = relationship('Trad', backref=backref('present'))

    def is_yourself_presents(self, uid):
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
            p = Present()
            p.book = book
            p.owner = owner
            with db.auto_commit():
                db.session.add(p)
