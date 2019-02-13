#!/usr/bin/env python
# -*- coding: utf-8 -*-
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

        # 重写filter


class DiyQuery(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(DiyQuery, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=DiyQuery)
from app.models.tradinfo import Trad
from app.models.book import _Base
from app.models.user import User
from app.models.book import Book
from app.models.wish import Wish
from app.models.present import Present
