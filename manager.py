#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.models import db
from wsgi import app

from app.models.user import User
from app.models.wish import Wish
from app.models.present import Present
from app.models.book import Book

manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def drop_db():
    print('清楚数据库......')
    db.drop_all(app=app)
    db.create_all(app=app)
    print('success')


@manager.command
def set_data():
    print('开始生成虚拟数据......')
    try:
        User.generate_fake(50)
        Book.generate_fake(50)
        Present.generate_fake(50)
        Wish.generate_fake(50)
    except Exception as e:
        raise e
    print('完成....')


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
