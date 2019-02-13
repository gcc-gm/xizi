#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
web = Blueprint('web', __name__)

from app.web import book
from app.web.user import user
from app.web import index
from app.web import wishes
from app.web import presents
from app.web.tradinfo import giver, requester, tradinfo
