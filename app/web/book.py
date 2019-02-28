#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.forms.book import SearchForm, UploadForm
from app.libs.helper import is_number_or_key
from app.libs.search import SearchBook
from app.libs.upload import filter_images
from app.models import Wish, Book, db
from app.viewmodels.book import BookCollection, BookViewModel
from app.web import web


@web.route('/search/book')
def search():
    collection_books = BookCollection()

    form = SearchForm(request.args)
    if form.validate():
        # strip()
        # 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
        # 注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
        q = form.q.data.strip()
        page = form.page.data

        number_or_key = is_number_or_key(q)
        search_book = SearchBook()

        if number_or_key == 'number':
            search_book.search_by_number(q)
        else:
            search_book.search_by_keyword(q)

        collection_books.fill(search_book, q)

        # 序列化一个对象，有对象的嵌套
        # return json.dumps(books, default=lambda obj: obj.__dict__)

    else:
        flash('搜索关键字错误！')
        # return jsonify({'msg': '参数错误！'})
    return render_template('search-result.html', books=collection_books.books, total=collection_books.total,
                           keyword=collection_books.keyword)


@web.route('/book/<number>/detail')
@login_required
def book_detail(number):
    wishes_note = []
    presents_note = []
    search_book = SearchBook()
    search_book.search_by_number(number)
    # search_book.books属性下存放book模型的集合--list
    book = search_book.first
    wishes_list = book.wishes
    presents_list = book.presents
    if wishes_list:
        # 得到所有的wish用户的模型
        wishes_note = [wish.owner for wish in wishes_list]
    if presents_list:
        # 得到所有的present用户的模型
        presents_note = [present.owner for present in presents_list]

    book = BookViewModel(book)

    return render_template('book-detail.html', book=book,
                           wishes_note=wishes_note, presents_note=presents_note)


@web.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_book():
    if current_user.student_id != '1602140129':
        flash("非法操作!")
        return redirect(url_for('web.recent'))

    form = UploadForm(request.form)
    if request.method == 'POST' and form.validate():
        upload_result = filter_images(form.number.data)
        if upload_result:
            with db.auto_commit():
                book = Book()
                book.set_attrs(form.data)
                book.image = upload_result
                db.session.add(book)
            flash('上传成功！')
            return render_template('upload.html', form=form)
        else:
            flash('失败!')
    return render_template('upload.html', form=form)
