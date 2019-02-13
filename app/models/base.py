#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, SmallInteger, Integer

from app.models import db


class _Base(db.Model):
    # 如果不设置这个属性就会报错， 因为SQLAlchemy
    __abstract__ = True
    create_time = Column('create_time', Integer)
    # 数据的状态码，用于实现软删除
    status = Column(SmallInteger, default=1)

    # 注意实例变量与类变量的区别
    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # 用于快速设置参数
    def set_attrs(self, attrs_dict):
        for key, values in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, values)

    # 用于格式化时间
    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
