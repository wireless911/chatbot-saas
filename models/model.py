# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-management_v2 -> model
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/7/14 14:19
@Desc   ：
==================================================
"""
from peewee import Model, CharField, DateTimeField, CompositeKey, PrimaryKeyField, TextField, IntegerField, \
    ForeignKeyField, SmallIntegerField
from datetime import datetime
from models import db


class RobotsModel(Model):
    class Meta:
        database = db
        db_table = "robots"

    id = PrimaryKeyField()
    bot_id = CharField(max_length=64)
    version = CharField(max_length=64)
    mode = CharField(max_length=64)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)


