#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app.forms.tradinfo import QQForm
from app.libs.enums import PendingStatus
from app.libs.send_mial import send_mail
from app.models import Trad, db, User, Book
from app.viewmodels.trad import in_trad
from app.web import web


@web.route('/give/book/<int:book_id>/<int:uid>')
@login_required
def give_book(book_id, uid):
    book = Book.query.get_or_404(book_id)
    requester = User.query.get_or_404(uid)
    if in_trad(current_user.id, book.id):
        flash('非法操作 !')
        return redirect(url_for('web.trad_info'))
    else:
        send_mail(requester.email, '赠送一本书', 'email/give_book.html',
                  book=book,
                  giver=current_user,
                  requester=requester)
        flash('你的赠送意愿已经发送至' + requester.email)
    return redirect(url_for('web.book_detail', number=book.number))


#
# @web.route('/ensure/agree/',methods=['POST','GET'])
# @login_required
# def ensure():
#     trad = Trad.query.filter_by(
#         giver_id=current_user.id, id=trad_id).first_or_404()
#     form = QQForm(request.form)
#     if request.method == "POST" and form.validate():
#         return ''
#
#     return render_template('agree_request.html',form=form)
#


# 同意
@web.route('/agree_trad/')
@login_required
def agree_trad(trad_id):
    """
          同意请求，只有书籍赠送者才可以同意请求
          注意需要验证超权
      """
    trad = Trad.query.filter_by(
        giver_id=current_user.id, id=trad_id).first_or_404()
    if trad.pending == PendingStatus.No_trad:
        if trad.pending == PendingStatus.Waiting:
            flash('你已经同意!')
            return redirect(url_for('web.trad_info'))

        with db.auto_commit():
            # give_id = current_user.id 这个条件可以防止超权
            trad.pending = PendingStatus.Waiting.value
        flash("操作成功!")
        return redirect(url_for('web.ensure'))
    else:
        flash('发生了一个错误 !')
    return redirect(url_for('web.trad_info'))


# 拒绝
@web.route('/Reject/<trad_id>')
@login_required
def Reject(trad_id):
    """
          拒绝请求，只有书籍赠送者才可以拒绝请求
          注意需要验证超权
      """
    trad = Trad.query.filter_by(
        giver_id=current_user.id, id=trad_id).first_or_404()

    if trad.pending == PendingStatus.Waiting:
        if trad.pending == PendingStatus.Reject:
            flash("你已经拒绝")
            return redirect(url_for('web.trad_info'))
        with db.auto_commit():
            requester = User.query.get_or_404(trad.requester_id)
            requester.star_value += 10
            trad.pending = PendingStatus.Reject.value
            trad.launched = 0
            flash("操作成功!")
    else:
        flash('发生了一个错误 !')
    return redirect(url_for('web.trad_info'))
