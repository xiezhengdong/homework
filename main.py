#!/usr/bin/env python

import os
import datetime

import tornado.web
import tornado.ioloop
from tornado.options import parse_command_line, define, options
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base

# 建立连接与数据库的连接
engine = create_engine('mysql+pymysql://seamile:54188@localhost:3306/homework')
Base = declarative_base(bind=engine)  # 创建模型的基础类
Session = sessionmaker(bind=engine)   # 创建会话类
session = Session()


class User(Base):
    '''类本身对应数据库里的表结构'''
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True)
    birthday = Column(Date, default=datetime.date(1990, 1, 1))
    city = Column(String(10), default='上海')
    money = Column(Float, default=0.0)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        q = session.query(User)
        users = q.limit(10)
        self.render('base.html', users=users)


class AllHandler(tornado.web.RequestHandler):
    def get(self):
        q = session.query(User)
        all_users = q.all()
        users = q.limit(10)
        self.render('all.html', all_users=all_users, users=users)


class InfoHandler(tornado.web.RequestHandler):
    def get(self):
        q = session.query(User)
        uid = int(self.get_argument('id'))
        user = q.get(uid)
        users = q.limit(10)
        self.render('info.html', user=user, users=users)


class ModifyHandler(tornado.web.RequestHandler):
    def get(self):
        q = session.query(User)
        uid = int(self.get_argument('id'))
        user = q.get(uid)
        users = q.limit(10)
        self.render('modify.html', user=user, users=users)

    def post(self):
        q = session.query(User)
        uid = int(self.get_argument('id'))
        user = q.get(uid)

        user.name = self.get_argument('name')
        user.birthday = self.get_argument('birthday')
        user.city = self.get_argument('city')
        user.money = float(self.get_argument('money'))
        session.commit()

        self.redirect('/info?id=%s' % uid)  # 通过重定向，跳转到用户信息页


def make_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    web_app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/info", InfoHandler),
            (r"/all", AllHandler),
            (r"/modify", ModifyHandler),

        ],
        template_path=os.path.join(base_dir, 'templates'),
        static_path=os.path.join(base_dir, 'statics')
    )
    return web_app


if __name__ == "__main__":
    define("host", default='localhost', help="主机地址", type=str)
    define("port", default=8000, help="主机端口", type=int)

    parse_command_line()

    app = make_app()
    app.listen(options.port, options.host)
    print('server running on %s:%s' % (options.host, options.port))

    loop = tornado.ioloop.IOLoop.current()
    loop.start()
