#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import desc

from app.libs.enums import PendingStatus
from app.models import Trad


class TradViewModel():

    def __init__(self, trad):
        self.id = trad.id

        self.book_title = trad.book.title
        self.book_author = trad.book.author
        self.book_publisher = trad.book.publisher
        self.book_price = trad.book.price
        self.book_number = trad.book.number
        self.book_image = trad.book.image
        self.book_number = trad.book.number

        self.time = trad.create_datetime

        self.requester_name = trad.requester_name
        self.requester_qq = trad.requester_qq
        self.requester_message = trad.requester_message

        self.giver_name = trad.giver_name
        self.giver_qq = ''

        self._pending = trad._pending
        self.pending = trad.pending
        self.status = self.pending_status()

    def pending_status(self):
        return PendingStatus.pending_str(self.pending)


def requester_trad(requester_id):
    sub_trad = Trad.query.filter_by(requester_id=requester_id).order_by(desc(Trad.create_time)).all()
    if sub_trad:
        return [TradViewModel(trad) for trad in sub_trad]
    return []


def giver_trad(giver_id):
    sub_trad = Trad.query.filter_by(giver_id=giver_id).order_by(desc(Trad.create_time)).all()
    if sub_trad:
        return [TradViewModel(trad) for trad in sub_trad]
    return []


def in_trad(uid, book_id):
    request = Trad.query.filter_by(requester_id=uid, book_id=book_id,launched=1).first()
    if request:
        return True
    giver = Trad.query.filter_by(giver_id=uid, book_id=book_id,launched=1).first()
    if giver:
        return True
    return False
