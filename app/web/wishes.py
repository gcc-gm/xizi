#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models import Wish, db
from app.viewmodels.book import BookViewModel
from app.viewmodels.trad import in_trad
from app.web import web


@web.route('/my_wishes')
@login_required
def my_wishes():
    wish_list_models = current_user.wishes
    wish_list = [BookViewModel(wish.book) for wish in wish_list_models]
    total = len(wish_list)
    return render_template('wish-list.html',
                           wish_list=wish_list,
                           total=total)


@web.route('/<int:book_id>/save_wishes_list')
@login_required
def save_to_wishes(book_id):
    note = current_user.can_save_list(book_id)

    if note['can_save']:
        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.book_id = note['book'].id
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    flash('成功加入心愿清单！')

    return redirect(url_for('web.book_detail', number=note['book'].number))


@web.route('/cancel_wishes/<book_id>')
@login_required
def cancel_wish_operation(book_id):
    wish = Wish.query.filter_by(book_id=book_id).first_or_404()
    if in_trad(current_user.id,book_id):
        flash("当前书籍正在交易中, 无法撤销")
        return redirect(url_for('web.trad_info'))
    if not wish:
        flash('该赠本不存在，删除失败')
    else:
        with db.auto_commit():
            wish.status = 0
            flash("撤销成功!")
    return redirect(url_for('web.my_wishes'))
