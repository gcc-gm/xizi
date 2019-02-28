#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash, abort
from flask_login import login_user, logout_user, login_required, current_user

from app.forms.email import EmailForm
from app.forms.user import RegisterForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from app.libs.send_mial import send_mail
from app.models.user import User
from app.web import web
from app.models import db


@web.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        flash('注册成功！')
        return redirect(url_for('web.login'))
    return render_template('register.html', form=form)


@web.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(student_id=form.student_id.data).first()
        if user and user.check_password(form.password.data):
            # 写入cookie，默认一次性的，即，浏览器关闭就失效
            login_user(user)
            # 登陆后自动跳回原来到原来的页面
            return_next = request.args.get('next')

            if not return_next or not return_next.startswith('/'):
                return_next = url_for('web.recent')
            return redirect(return_next)
        else:
            flash('账号不存在或密码错误！')
    return render_template('login.html', form=form)


@web.route('/personal')
@login_required
def personal():
    return render_template('personal.html', user=current_user,
                           wishes_total=len(current_user.wishes),
                           presents_total=len(current_user.presents))


@web.route('/email_binding')
@login_required
def email_bind():
    if current_user._email_bind:
        flash('禁止操作!')
        return redirect(url_for('web.personal'))
    from app.libs.helper import email_bind
    verification_code = email_bind()
    token = current_user.generate_token(verification_code=verification_code)
    send_mail(current_user.email, '绑定你的邮箱', 'email/binding_email.html',
              code=verification_code)
    flash('已发送将验证码发送至邮箱: ' + str(current_user.email))
    return redirect(url_for('web.set_binding', token=token, _external=True))


@web.route('/set_binding/<token>', methods=['POST', 'GET'])
@login_required
def set_binding(token):
    code = request.form.get('code')
    if request.method == 'POST' and code == current_user.get_verification_code(token):
        success = current_user.binding_email(token)
        if success:
            flash('邮箱绑定成功！')
            return redirect(url_for('web.personal'))
        else:
            flash('重置失败！')

    return render_template('email_bind.html', code=code)


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        current_user.password = form.new_password1.data
        db.session.commit()
        flash('密码已更新成功')
        return redirect(url_for('web.personal'))
    return render_template('change_password.html', form=form)


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.recent'))


@web.route('/reset/password/request', methods=['POST', 'GET'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        user_email = form.email.data
        user = User.query.filter_by(email=user_email).first_or_404()
        send_mail(form.email.data, '重置你的密码',
                  'email/reset_password.html', user=user,
                  token=user.generate_token())
        flash('一封邮件已发送到邮箱' + user_email + '，请及时查收')
        return redirect(url_for('web.recent'))
    return render_template('forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('web.recent'))
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        result = User.reset_password(token, form.password1.data)
        if result:
            flash('你的密码已更新,请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('服务器发生未知错误！')
    return render_template('reset_password.html', form=form)


@web.route('/star_value')
@login_required
def not_enough_value():
    if current_user.star_value >= 20:
        return redirect(url_for('web.recent'))
    return render_template('about_star.html', star_value=current_user.star_value)


