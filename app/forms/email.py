#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms import Form, StringField
from wtforms.validators import Email, DataRequired, Length, ValidationError

from app.models import User


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范！')])

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError("请检查是否是你的邮箱")
        if user.email_bind == '未绑定':
            raise ValidationError('邮箱未绑定')
