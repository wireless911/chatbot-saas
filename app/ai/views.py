import asyncio
import functools
import traceback
from typing import Dict, Optional, Text

from rasa.server import validate_request_body
from sanic.request import Request

from sanic.views import HTTPMethodView
from sanic.log import logger as _logger

from sanic.response import json, stream
from sanic_openapi import doc

from config.settings import PUB_ACTION
from utils.context import PathContext
from app.ai.swagger import TrainDoc, PublishDoc, ParseDoc, ChatDoc


class ModelTrainViews(HTTPMethodView):
    """模型训练视图"""

    @doc.consumes(TrainDoc, location="body")
    @doc.description('模型训练')
    @doc.summary('模型训练')
    async def post(self, request: Request):
        async def streaming_fn(response):
            app = request.app
            validate_request_body(
                request,
                "You must provide training data in the request body in order to "
                "train your models.",
            )
            rjs = request.json
            path_context = PathContext(rjs)

            # create a temporary directory to store config, domain and
            # training data

            try:
                with app.active_training_processes.get_lock():
                    app.active_training_processes.value += 1

                info = dict(
                    domain=path_context.domain_path,
                    config=path_context.config_file_path,
                    training_files=path_context.root_path,
                    output=path_context.chatbot_model_path,
                    force_training=rjs.get("force", False),
                )

                loop = asyncio.get_event_loop()

                # from rasa import train as train_model
                from core.train import train as train_model
                await response.write({"code": 200, "msg": "train task push in queue"})

                # Declare `model_path` upfront to avoid pytype `name-error`
                model_path: Optional[Text] = None
                # pass `None` to run in default executor
                model_path = await loop.run_in_executor(
                    None, functools.partial(train_model, **info)
                )
                # # reload agent
                # bot = app.botsManager.ai[path_context.bot_id]  # type:BotManager
                # app.botsManager.ai[path_context.bot_id] = await bot.load_agent(model_path=model_path)
            except Exception as e:
                _logger.info(traceback.format_exc())
                await response.write({"code": 500, "msg": "train error"})
            finally:
                with app.active_training_processes.get_lock():
                    app.active_training_processes.value -= 1

                await response.write({"code": 200, "msg": "ok2"})

        return stream(streaming_fn, content_type="application/json")


class ModelPublishViews(HTTPMethodView):
    """模型发布视图"""

    @doc.consumes(PublishDoc, location="body")
    @doc.description('模型发布')
    @doc.summary('模型发布')
    async def post(self, request: Request):
        app = request.app
        rjs = request.json
        res = await self.publish(app, msg=rjs)
        if not res:
            return json({"code": 400, "data": "publish error"})
        return json({"code": 200, "data": "ok"})

    async def publish(self, app, msg: Optional[Dict] = None):
        try:
            action = PUB_ACTION.format(msg["mode"])
            flag = await app.pub.publish_json(action, msg)
            assert flag == app.workers
        except Exception as e:
            _logger.error(e)
            _logger.warning(f"{msg} publish error")
            return None
        return True


class ModelParseViews(HTTPMethodView):
    @doc.consumes(ParseDoc, location="body")
    @doc.description('语句解析')
    @doc.summary('语句解析')
    async def post(self, request: Request):
        req = request.json
        bot_id = req.get("bot_id")
        bot = request.app.botsManager.bots[bot_id]  # type:BotManager
        response = await bot.parse(req.get("question"))
        return json({"code": 200, "data": response})


class ModelChatViews(HTTPMethodView):
    @doc.consumes(ChatDoc, location="body")
    @doc.description('聊天接口')
    @doc.summary('聊天接口')
    async def post(self, request: Request):
        req = request.json
        bot_id = req.get("bot_id")
        sender_id = req.get("sender_id")
        bot = request.app.botsManager.bots[bot_id]  # type:BotManager
        response = await bot.handle_text(req.get("question"), sender_id=sender_id)

        return json({"code": 200, "data": response}, ensure_ascii=False)
