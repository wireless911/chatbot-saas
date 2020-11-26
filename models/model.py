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
import inspect
import json
import sys

from peewee import Model, CharField, DateTimeField, CompositeKey, PrimaryKeyField, TextField, IntegerField, \
    BooleanField, \
    ForeignKeyField, SmallIntegerField, AutoField

from datetime import datetime
from models import db
from models.fields import JsonField


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def migrate(cls):
        """数据库迁移"""
        return cls.create_table(True)


class UserModel(BaseModel):
    """用户模型"""

    class Meta:
        db_table = "user"

    id = AutoField()
    username = CharField(max_length=64)
    password = CharField(max_length=64)
    scopes = CharField(max_length=64)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)

    def to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "password": self.password,
            "scopes": self.scopes
        }


class RobotModel(BaseModel):
    """机器人模型"""

    class Meta:
        db_table = "robot"

    id = AutoField()
    name = CharField(max_length=64)
    create_time = DateTimeField(default=datetime.now,formats='%Y-%m-%d %H:%M:%S')
    update_time = DateTimeField(default=datetime.now)
    is_deleted = BooleanField(default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name":self.name,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            "is_deleted": self.is_deleted
        }


class IntentModel(BaseModel):
    class Meta:
        db_table = "intent"

    id = AutoField()
    name = CharField(max_length=64)
    name_en = CharField(max_length=64)
    robot_id = IntegerField()
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)


class SentenceModel(BaseModel):
    class Meta:
        db_table = "sentence"

    id = AutoField()
    sentences = CharField(max_length=512)
    intent_id = IntegerField()
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)


class FaqModel(BaseModel):
    class Meta:
        db_table = "faq"

    id = AutoField()
    name = CharField(max_length=255)
    questions = JsonField()
    answers = JsonField()
    robot_id = IntegerField()
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)


class RasaModel(BaseModel):
    class Meta:
        db_table = "rasa_model"

    id = AutoField()
    description = CharField(max_length=255)
    version = CharField(max_length=64)
    mode = CharField(max_length=64)
    status = IntegerField()
    robot_id = IntegerField()
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)
