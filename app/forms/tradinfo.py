#!/usr/bin/env python
# -*- coding: utf-8 -*-
# address = Column(String(100), nullable=False)
# message = Column(String(100))
# mobile = Column(String(11), nullable=False)
from wtforms import Form, StringField
from wtforms.validators import DataRequired, Regexp


class TradForm(Form):
    requester_qq = StringField(validators=[DataRequired(message='qq号不能为空')])
    requester_message = StringField(validators=[DataRequired(message='留言不能为空')])
    requester_mobile = StringField(validators=[DataRequired(message='手机号不能为空！'),
                                               Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])


class QQForm(Form):
    giver_qq = StringField(validators=[DataRequired(message='qq号不能为空')])
