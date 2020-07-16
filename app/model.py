import asyncio
import functools
import os
import tempfile
import traceback
from typing import Dict, Optional, Text
import collections

import rasa
import ujson
from rasa.constants import DEFAULT_DOMAIN_PATH, DEFAULT_MODELS_PATH
from rasa.core.agent import Agent
from rasa.core.domain import InvalidDomain
from rasa.server import validate_request_body, ErrorResponse
from sanic import response
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.log import logger as _logger

from sanic.response import json, stream

from core.bots import BotManager
from utils.context import PathContext


class ModelTrainViews(HTTPMethodView):
    """模型训练视图"""

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
                    training_files=path_context.chatbot_train_root_path,
                    output=path_context.chatbot_model_root_path,
                    force_training=rjs.get("force", False),
                )

                loop = asyncio.get_event_loop()

                from rasa import train as train_model
                await response.write({"msg": "ok1"})

                # Declare `model_path` upfront to avoid pytype `name-error`
                model_path: Optional[Text] = None
                # pass `None` to run in default executor
                model_path = await loop.run_in_executor(
                    None, functools.partial(train_model, **info)
                )
                # reload agent
                bot = app.bots[path_context.bot_id]  # type:BotManager
                app.bots[path_context.bot_id] = await bot.load_agent(model_path=model_path)
            except InvalidDomain as e:
                raise ErrorResponse(
                    400,
                    "InvalidDomainError",
                    f"Provided domain file is invalid. Error: {e}",
                )
            except Exception as e:
                _logger.debug(traceback.format_exc())
                raise ErrorResponse(
                    500,
                    "TrainingError",
                    f"An unexpected error occurred during training. Error: {e}",
                )
            finally:
                with app.active_training_processes.get_lock():
                    app.active_training_processes.value -= 1

                await response.write({"msg": "ok2"})

        return stream(streaming_fn, content_type="application/json")


class ModelParseViews(HTTPMethodView):

    async def post(self, request: Request):
        req = request.json
        bot_id = req.get("bot_id")
        bot = request.app.bots[bot_id]  # type:BotManager
        response = await bot.parse(req.get("question"))

        return json({"code": 200, "data": response})


class ModelChatViews(HTTPMethodView):

    async def post(self, request: Request):
        req = request.json
        bot_id = req.get("bot_id")
        sender_id = req.get("sender_id")
        bot = request.app.bots[bot_id]  # type:BotManager
        response = await bot.handle_text(req.get("question"), sender_id=sender_id)

        return json({"code": 200, "data": response}, ensure_ascii=False)
