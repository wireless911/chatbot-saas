#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> swagger
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/9/18 10:31
@Desc   ：
==================================================
"""
from sanic_openapi import doc




BotDoc = doc.String(description="bot_id", required=True, name="bot_id", choices=["rasa-demo"])
