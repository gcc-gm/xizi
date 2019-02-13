#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.libs.enums import PendingStatus
from app.models import Book, Trad, db
from app.viewmodels.trad import requester_trad, giver_trad
from app.web import web


@web.route('/trad_info')
@login_required
def trad_info():
    request_trad = requester_trad(current_user.id)
    give_trad = giver_trad(current_user.id)
    total = len(request_trad) + len(give_trad)
    return render_template('trad_info.html', give_trad=give_trad,
                           request_trad=request_trad,
                           total=total)
