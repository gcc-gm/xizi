#!/usr/bin/env python
# -*- coding: utf-8 -*-
DIALECT = 'mysql'
DRIVE = 'pymysql'
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
