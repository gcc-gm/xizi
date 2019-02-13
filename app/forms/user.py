#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms import StringField, Form, PasswordField
from wtforms.validators import DataRequired, Length, \
    Email, ValidationError, EqualTo, Regexp

from app.models.user import User


class RegisterForm(Form):
    name = StringField('昵称', validators=[
        DataRequired(message='不能为空！'), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范！')])

    password = PasswordField('输入密码', validators=[
        DataRequired(), Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(), Length(6, 20)])

    student_id = StringField(validators=[DataRequired(message='学号不能为空'),
                                         Regexp('^1[0-9]{9}$', 0, '请输入正确的学号')])
    phone_number = StringField(validators=[DataRequired(message='手机号不能为空！'),
                                           Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册!')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('昵称已存在!')

    def validate_phone_number(self, field):
        if User.query.filter_by(phone_number=field.data).first():
            raise ValidationError('手机号已被注册!')

    def validate_student_id(self, field):
        if User.query.filter_by(student_id=field.data).first():
            raise ValidationError('该学号已存在！')


class LoginForm(Form):
    student_id = StringField(validators=[DataRequired(),
                                         Regexp('^1[0-9]{9}$', 0, '请输入正确的学号')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20)])


class ChangePasswordForm(Form):
    old_password = PasswordField('原有密码', validators=[DataRequired()])
    new_password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 10, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField('确认新密码字段', validators=[DataRequired()])


class ResetPasswordForm(Form):
    password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(), Length(6, 20)])
