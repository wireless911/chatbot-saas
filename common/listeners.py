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
from rasa.core.agent import load_agent, Agent
from sanic import Sanic
from typing import Optional, List
from sanic.log import logger as _logger

from core.bots import BotManager
from models import dbManger
from models.model import RobotsModel


async def before_server_start(app: Sanic, loop):
    from config.settings import MODE
    bots = await dbManger.execute(RobotsModel.select().where(RobotsModel.mode == MODE))
    bot: Optional[RobotsModel] = None

    app.bots = {}
    for bot in bots:
        from utils.context import PathContext
        path_context = PathContext({"bot_id": bot.bot_id, "version": bot.version})
        app.bots[bot.bot_id] = await BotManager(path_context).load_agent()
