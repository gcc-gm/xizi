#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Boolean

from app.libs.enums import PendingStatus
from app.models.base import _Base


class Trad(_Base):
    """
        一次具体的交易信息
    """
    __tablename__ = 'trad'

    # 邮寄信息
    id = Column(Integer, primary_key=True)
    # uid = Column(Integer, ForeignKey('users.id'), nullable=False)
    launched = Column(SmallInteger, default=1)
    # 书籍信息
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)

    # 请求者信息
    requester_id = Column(Integer,nullable=False)
    requester_name = Column(String(15))
    requester_qq = Column(String(11), nullable=False)
    requester_mobile = Column(String(11), nullable=False)
    requester_message = Column(String(100))
    # 赠送者信息
    giver_id = Column(Integer,nullable=False)
    giver_name = Column(String(15),nullable=False)

    # 交易状态信息
    _pending = Column('pending', SmallInteger, default=0)

    # 还有book属性

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status
