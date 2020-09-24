#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> channels
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/8/26 17:13
@Desc   ：
==================================================
"""
from urllib.parse import urljoin

from rasa.core.channels.channel import RestInput, UserMessage, CollectingOutputChannel
import inspect
from asyncio import CancelledError
from sanic import Blueprint, response, Sanic
from sanic.request import Request
from typing import Text, Callable, Awaitable, List, Optional
from sanic.log import logger
import rasa.utils.endpoints
from sanic.response import HTTPResponse


def register(bot_id: Optional[Text],
             input_channels: List["InputChannel"],
             app: Sanic, route: Optional[Text]
             ) -> None:
    async def handler(*args, **kwargs):
        await app.bots[bot_id].handle_message(*args, **kwargs)

    for channel in input_channels:
        if route:
            p = urljoin(route, channel.url_prefix())
        else:
            p = None
        app.blueprint(channel.blueprint(handler), url_prefix=p)

    app.input_channels = input_channels


class MyRestInput(RestInput):
    """自定义渠道"""

    @classmethod
    def name(cls) -> Text:
        return "my_channel"

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        # noinspection PyUnusedLocal
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = await self._extract_sender(request)
            text = self._extract_message(request)
            should_use_stream = rasa.utils.endpoints.bool_arg(
                request, "stream", default=False
            )
            input_channel = self._extract_input_channel(request)
            metadata = self.get_metadata(request)

            if should_use_stream:
                return response.stream(
                    self.stream_response(
                        on_new_message, text, sender_id, input_channel, metadata
                    ),
                    content_type="text/event-stream",
                )
            else:
                collector = CollectingOutputChannel()
                # noinspection PyBroadException
                try:
                    await on_new_message(
                        UserMessage(
                            text,
                            collector,
                            sender_id,
                            input_channel=input_channel,
                            metadata=metadata,
                        )
                    )
                except CancelledError:
                    logger.error(
                        "Message handling timed out for "
                        "user message '{}'.".format(text)
                    )
                except Exception:
                    logger.exception(
                        "An exception occured while handling "
                        "user message '{}'.".format(text)
                    )
                return response.json(collector.messages)

        return custom_webhook
