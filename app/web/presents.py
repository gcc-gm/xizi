#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.models import db, Present
from app.viewmodels.book import BookViewModel
from app.viewmodels.trad import in_trad
from app.web import web


@web.route('/my_presents')
@login_required
def my_presents():
    present_list_models = current_user.presents
    present_list = [BookViewModel(present.book) for present in present_list_models]
    total = len(present_list)
    return render_template('presents-list.html',
                           present_list=present_list,
                           total=total)


@web.route('/<int:book_id>/save_presents_list')
@login_required
def save_to_presents(book_id):
    note = current_user.can_save_list(book_id)
    if note['can_save']:
        with db.auto_commit():
            present = Present()
            present.uid = current_user.id
            present.book_id = note['book'].id
            db.session.add(present)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    flash('成功加入赠送清单！')
    return redirect(url_for('web.book_detail', number=note['book'].number))


@web.route('/cancel_presents/<book_id>')
@login_required
def cancel_present_operation(book_id):
    present = Present.query.filter_by(uid=current_user.id, book_id=book_id).first_or_404()
    if in_trad(current_user.id,book_id):
        flash("当前书籍正在交易中, 无法撤销")
        return redirect(url_for('web.trad_info'))
    if not present:
        flash('该心愿不存在，删除失败')
    else:
        with db.auto_commit():
            present.status = 0
            flash("撤销成功!")
    return redirect(url_for('web.my_presents'))
