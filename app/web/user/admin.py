#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import abort

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.libs.upload import re_book_image
from app.models import User, Trad, Present, Wish, db, Book
from app.viewmodels.book import BookViewModel
from app.web import web


@web.route('/admin')
@login_required
def admin():
    if current_user.student_id != '1602140129':
        abort(404)
    users = User.query.all()
    trads = Trad.query.all()
    presents = Present.query.all()
    wishes = Wish.query.all()
    books = Book.query.all()
    if books:
        books = [BookViewModel(book) for book in books]
    if users:
        users = [user.intro for user in users]

    return render_template('admin.html', users=users, books=books,
                           trads=trads, presents=presents,
                           wishes=wishes)


@web.route('/admin/del_wish/<int:wid>')
@login_required
def del_wish(wid):
    if current_user.student_id != '1602140129':
        abort(404)

    wish = Wish.query.filter_by(status=0, uid=wid).first_or_404()
    with db.auto_commit():
        db.session.delete(wish)
        flash('success!')
    return redirect(url_for('web.admin'))


@web.route('/admin/del_present/<int:pid>')
@login_required
def del_present(pid):
    if current_user.student_id != '1602140129':
        abort(404)

    present = Present.query.filter_by(status=0, uid=pid).first_or_404()
    with db.auto_commit():
        db.session.delete(present)
        flash('success!')
    return redirect(url_for('web.admin'))


@web.route('/admin_del_book/<int:bid>/<string:image>')
@login_required
def del_book(bid, image):
    if current_user.student_id != '1602140129':
        abort(404)
    book = Book.query.get_or_404(bid)
    if not re_book_image(image):
        flash('系统找不到图片!')
    with db.auto_commit():
        db.session.delete(book)
        flash('success!')
    return redirect(url_for('web.admin'))


@web.route('/admin_del_trad/<int:trad_id>')
@login_required
def del_trad(trad_id):
    if current_user.student_id != '1602140129':
        abort(404)
    trad = Trad.query.get_or_404(trad_id)
    with db.auto_commit():
        db.session.delete(trad)
    return redirect(url_for('web.admin'))


@web.route('/admin_del_user/<int:uid>')
@login_required
def del_user(uid):
    if current_user.student_id != '1602140129':
        abort(404)
    user = User.query.get_or_404(uid)
    if user.student_id == '1602140129':
        flash('禁止!')
        return redirect(url_for('web.admin'))
    with db.auto_commit():
        db.session.delete(user)
        flash('success!')
    return redirect(url_for('web.admin'))
