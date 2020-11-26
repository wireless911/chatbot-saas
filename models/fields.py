#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> fields
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/11/13 14:44
@Desc   ：
==================================================
"""
import json

from peewee import Field


class JsonField(Field):
    """自定义字段(json类型)"""
    field_type = 'json'

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)