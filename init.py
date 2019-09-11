#!/usr/bin/env python

from main import Base, Session, User

# 创建表结构和数据
Base.metadata.create_all()

# 定义数据
bob = User(name='bob', birthday='1990-3-21', city='上海', money=370)
tom = User(name='tom', birthday='1995-9-12', money=288)
lucy = User(name='lucy', birthday='1998-5-14', city='北京')
jam = User(name='jam', birthday='1994-3-9', city='深圳', money=86)
alex = User(name='alex', birthday='1992-3-17', city='北京')
eva = User(name='eva', birthday='1987-7-28', city='深圳', money=631)
rob = User(name='rob', birthday='1974-2-5', city='上海', money=735)
ella = User(name='ella', birthday='1999-5-26', city='北京')
tony = User(name='tony', city='深圳', money=199)

# 在数据库中添加数据
session = Session()  # 创建会话
session.add_all([bob, tom, lucy, jam, alex, eva, rob, ella, tony])
session.commit()
