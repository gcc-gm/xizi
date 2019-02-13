#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.forms.tradinfo import TradForm
from app.libs.enums import PendingStatus
from app.libs.send_mial import send_mail
from app.models import User, Book, db
from app.web import web
from app.models.tradinfo import Trad


@web.route('/requester/book/<number>/<int:uid>', methods=['POST', 'GET'])
@login_required
def request_book(number, uid):
    giver = User.query.get_or_404(uid)
    requester = User.query.get_or_404(current_user.id)
    book = Book.query.filter_by(number=number).first_or_404()

    if not giver.can_make_trad(book.id):
        flash('该书籍正在交易')
        return redirect(url_for('web.book_detail', number=book.number))

    if requester.enough_star():
        flash("你的星愿值不足,送出图书可以获得星愿值")
        return redirect(url_for('web.not_enough_value'))

    giver_have_present = giver.book_in_presents(book.id)
    if not giver_have_present:
        flash('所请求的用户并没有赠送此书')
        return redirect(url_for('web.book_detail', number=book.number))

    current_wishes = requester.book_in_wishes(book.id)
    if not current_wishes:
        flash('系统没有在你的心愿清单里找到该书')
        return redirect(url_for('web.my_wishes'))

    form = TradForm(request.form)
    trad = Trad()

    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            try:
                form.populate_obj(trad)
            except Exception as e:
                raise e

            trad.book_id = book.id

            trad.requester_id = requester.id
            trad.requester_name = requester.name

            trad.giver_id = giver.id
            trad.giver_name = giver.name

            requester.star_value -= 10
            db.session.add(trad)
        send_mail(giver.email,'请求一本书','email/request_book.html',
                  title=book.title,requester=current_user.name,giver=giver.name)
        flash('成功')
        return redirect(url_for('web.trad_info'))
    return render_template('request_trad.html', form=form, requester=requester, giver=giver)


# 撤销
@web.route('/Redraw/<trad_id>')
@login_required
def Redraw(trad_id):
    """
          撤销请求，只有书籍请求者才可以撤销请求
          注意需要验证超权
      """
    trad = Trad.query.filter_by(
        requester_id=current_user.id, id=trad_id).first_or_404()
    if trad.pending == PendingStatus.Waiting:
        if trad.pending == PendingStatus.Redraw:
            flash("你已经撤销")
            return redirect(url_for('web.recent'))
        with db.auto_commit():
            current_user.star_value += 10
            trad.pending = PendingStatus.Redraw.value
            trad.launched = 0
        flash("操作成功!")
    else:
        flash('发生了一个错误 !')
    return redirect(url_for('web.trad_info'))


# 完成心愿
@web.route('/Success/<trad_id>')
@login_required
def Success(trad_id):
    """
          完成交易，只有请求者才能确定
          注意需要验证超权
      """
    trad = Trad.query.filter_by(
        requester_id=current_user.id, id=trad_id).first_or_404()

    if trad.pending == PendingStatus.Waiting:
        if trad.pending == PendingStatus.Success:
            flash("交易已经完成")
            return redirect(url_for('web.trad_info'))
        with db.auto_commit():
            trad.pending = PendingStatus.Success.value
            giver = User.query.get(trad.giver_id)
            giver.love_value += 10
            trad.launched = 0
        flash('操作成功 ! ')

    else:
        flash('发生了一个错误 !')
    return redirect(url_for('web.trad_info'))
