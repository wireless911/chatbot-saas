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


class TrainDoc:
    bot_id = doc.String(description="bot_id", required=True, name="bot_id", choices=["rasa-demo"])
    sender_id = doc.String(description="sender_id", required=True, name="sender_id", choices=["fjdsafjdsfjdsi"])


class PublishDoc:
    bot_id = doc.String(description="bot_id", required=True, name="bot_id", choices=["rasa-demo"])
    mode = doc.String(description="mode", required=True, name="mode", choices=["test", "product"])


class ParseDoc:
    bot_id = doc.String(description="bot_id", required=True, name="bot_id", choices=["rasa-demo"])
    question = doc.String(description="question", required=True, name="question", choices=["hello", "bye"])

class ChatDoc:
    bot_id = doc.String(description="bot_id", required=True, name="bot_id", choices=["rasa-demo"])
    question = doc.String(description="question", required=True, name="question", choices=["hello", "bye"])
    channel = doc.String(description="channel", required=False, name="channel", choices=["wx", "ec"])
    conversion_id = doc.String(description="conversion_id", required=False, name="conversion_id", choices=["fdjsajfdisjfdj"])
    user_id = doc.String(description="user_id", required=False, name="user_id", choices=["fjdsafjdsfjdsi"])