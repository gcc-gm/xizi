#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'web.login'
login_manager.login_message = '请先登陆或注册'

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    # 注册蓝图
    from app.web import web
    app.register_blueprint(web)

    # 注册login_manager
    login_manager.init_app(app)

    # 注册SQLAlchemy
    from app.models.base import db
    db.init_app(app)
    # db.drop_all(app=app)
    db.create_all(app=app)

    # 注册邮件插件
    mail.init_app(app)

    return app
