#!/usr/bin/env python
# -*- coding: utf-8 -*-
DIALECT = 'mysql'
DRIVE = 'cymysql'
USERNAME = 'root'
PASSWORD = 'ddd123'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'xizi'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVE, USERNAME, PASSWORD, HOST, PORT, DATABASE )
SQLALCHEMY_TRACK_MODIFICATIONS = False
# secret_key
SECRET_KEY = 'abc_sf_SF_SD_SD_FCS_s'


# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'gccgm8564@qq.com'
MAIL_PASSWORD = 'coyoxylcewaqbbba'
MAIL_SUBJECT_PREFIX = '[西子]'
MAIL_SENDER = '**'
