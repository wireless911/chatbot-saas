import asyncio
import functools
import traceback
from typing import Dict, Optional, Text

from sanic.request import Request

from sanic.views import HTTPMethodView
from sanic.log import logger as _logger

from sanic.response import json
from sanic_openapi import doc
from app.bots.swagger import BotDoc
from common.response import Response
from models import dbManger
from models.model import RobotModel


class BotsViews(HTTPMethodView):
    """机器人列表"""

    @doc.description('机器人列表')
    @doc.summary('机器人列表')
    async def get(self, request: Request):
        bots = await dbManger.execute(RobotModel.select())
        bots = [bot.to_dict() for bot in bots]
        return Response(data=bots, status=200, message="ok")

    @doc.description('添加机器人')
    @doc.summary('添加机器人')
    async def post(self, request: Request):
        form_data = request.form



        return Response(data=None, status=200, message="ok")


class BotViews(HTTPMethodView):
    """机器人"""

    @doc.description('机器人')
    @doc.summary('机器人')
    async def get(self, request: Request, id):

        try:
            bot = await dbManger.get(RobotModel, id=id)
            _logger.warning(traceback.format_exc())
        except Exception as e:
            bot = None

        if not bot:
            return Response(data=bot, status=200, message="ok")
        return Response(data=bot.to_dict(), status=200, message="ok")

