#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.helper import is_number_or_key
from app.models import db
from app.models.book import Book
from app.models.base import _Base
from app.models.tradinfo import Trad

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(_Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)
    phone_number = Column(String(11), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    student_id = Column(String(10), nullable=False)
    _email_bind = Column(Boolean, default=False)
    # 爱心值
    love_value = Column(Integer, default=80)
    # 星愿值
    star_value = Column(Integer, default=80)

    # 该用户所有的心愿，得到其所有的心愿模型，一个列表
    _wishes = relationship('Wish', backref=backref('owner'))
    # 同上
    _presents = relationship('Present', backref=backref('owner'))

    # 同上
    # _sub_trad = relationship('Trad', backref=backref('owner'))

    @property
    def email_bind(self):
        if self._email_bind:
            return '已绑定'
        return '未绑定'

    # @property
    # def sub_trad(self):
    #     if self._sub_trad:
    #         return [trad for trad in self._sub_trad if trad.status == 1]
    #     return []

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

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 利用此函数来实现验证， 返回的是True, False
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def generate_token(self, expiration=600, **keyword):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # 存入ID号， 其实存任意的信息都可以
        note = dict(keyword)
        note['id'] = self.id
        temp = s.dumps(note).decode('utf-8')
        # temp为byte,故要编码
        return temp

    def verify_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return None
        if self.id == data.get('id'):
            return data

    def binding_email(self, token):
        data = self.verify_token(token)
        if data:
            with db.auto_commit():
                self._email_bind = True
        else:
            return False
        return True

    def get_verification_code(self, token):
        verification_code = ''
        data = self.verify_token(token)
        if data:
            verification_code = data.get('verification_code')
        return str(verification_code)

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get_or_404(uid)
            user.password = new_password
        return True

    def can_save_list(self, book_id):
        book = Book.query.get_or_404(book_id)
        note = dict(
            can_save=False,
            book=book
        )
        if not book:
            return note
        wishes_book_models = [wish.book for wish in self.wishes if self.wishes]
        presents_book_models = [present.book for present in self.presents if self.presents]

        if (book not in presents_book_models) \
                and (book not in wishes_book_models):
            note['can_save'] = True
            return note

        return note

    def book_in_wishes(self, book_id):
        find_book = Book.query.get_or_404(book_id)
        if not find_book:
            return False

        wishes_list = self.wishes
        if wishes_list:
            wishes_book_models = [wish.book for wish in wishes_list]
            if find_book in wishes_book_models:
                return True
        return False

    def book_in_presents(self, book_id):
        find_book = Book.query.get_or_404(book_id)
        if not find_book:
            return False

        presents_list = self.presents
        if presents_list:
            present_book_models = [present.book for present in presents_list]
            if find_book in present_book_models:
                return True
        return False

    def enough_star(self):
        if self.star_value >= 10:
            return False
        return True

    def can_make_trad(self, book_id):
        tem = Trad.query.filter_by(giver_id=self.id, book_id=book_id).first()
        if tem:
            return False
        return True

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User()
            u.name = forgery_py.internet.user_name(True),
            u.email = forgery_py.internet.email_address(),
            u.password = forgery_py.lorem_ipsum.word()
            u.phone_number = str(15778118000 + i)
            u.student_id = str(160214000 + i)
            with db.auto_commit():
                db.session.add(u)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)
