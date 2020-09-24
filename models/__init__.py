#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-management_v2 -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/7/14 14:19
@Desc   ：
==================================================
"""

from peewee_async import Manager, PooledMySQLDatabase
from config.settings import MYSQL_PARAMS

db = PooledMySQLDatabase(**MYSQL_PARAMS)

dbManger = Manager(db)
