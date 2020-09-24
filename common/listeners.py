#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：rates_address -> listenners
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/6/12 12:25
@Desc   ：
==================================================
"""
import time

import aioredis
from aioredis import Redis
from rasa.core.agent import load_agent, Agent
from sanic import Sanic
from typing import Optional, List
from sanic.log import logger as _logger
from config.settings import SUB_ACTION, SUB_ACTION_REDIS_PASS, REDIS_URL
from core.bots import BotsManager
import asyncio


async def before_server_start(app: Sanic, loop):
    app.botsManager = await BotsManager(app.mode).load_bots()
    app.pub = await aioredis.create_redis(REDIS_URL, **SUB_ACTION_REDIS_PASS)


async def after_server_start(app: Sanic, loop):
    # reload chatbot
    async def reload_chatbot(ch):
        while (await ch.wait_message()):
            msg = await ch.get_json()
            botsManager = app.botsManager  # type:BotsManager
            await botsManager.publish(msg["bot_id"])

    # 订阅redis channel
    app.sub = await aioredis.create_redis(REDIS_URL, **SUB_ACTION_REDIS_PASS)
    _logger.info(f"sub {SUB_ACTION} in redis")

    res = await app.sub.subscribe(SUB_ACTION)
    tsk = asyncio.ensure_future(reload_chatbot(res[0]))
    await tsk
