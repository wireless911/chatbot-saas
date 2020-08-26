#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-management_v2 -> bots
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/7/14 17:38
@Desc   ：
==================================================
"""
import os
from typing import Optional, Text

from rasa.core.agent import load_agent, Agent
from rasa.core.brokers.broker import EventBroker
from rasa.core.brokers.file import FileEventBroker
from rasa.core.channels import UserMessage
from rasa.core.lock_store import LockStore
from rasa.core.tracker_store import TrackerStore
from rasa.core.utils import AvailableEndpoints
from rasa.model import get_model_subdirectories

# from models import dbManger
from models.model import RobotsModel
from sanic.log import logger as _logger

from utils.context import PathContext


class BotManager(object):

    def __init__(self,
                 path_context: PathContext,
                 agent: Agent = None,
                 ):
        ''' agent manager
         Args:
        model: Path to model archive.
        endpoints: Path to endpoints file.
        credentials: Path to channel credentials file.
        '''
        self.path_context = path_context
        endpoints_path = self.path_context.endpoints_file_path
        credentials_path = self.path_context.credentials_file_path

        self.agent = agent if agent else None

        # broker tracker
        # read file if have endpoints file otherwise use default setting
        if os.path.exists(endpoints_path):
            # load endpoints
            self._load_endpoints(endpoints=endpoints_path)
        else:
            # create event broker
            event_broker = FileEventBroker()  # TODO 修改这里的broker，file格式的不太适合生产
            # create tracker store
            from config.settings import REDIS_SETTING
            self.tracker_store = TrackerStore(**REDIS_SETTING, event_broker=event_broker)

    async def load_agent(self, model_path: Optional[Text] = None):
        """
        加载agent ,重载agent
        :param model_path:
        :return:
        """
        model_path = self.path_context.chatbot_model_path if not model_path else model_path
        self.agent = await load_agent(
            model_path=model_path,
            generator=self.generator,
            tracker_store=self.tracker_store,
            lock_store=self.lock_store,
            action_endpoint=self.action_endpoint,

        )
        _logger.info(f"reload robot {self.path_context.bot_id}")
        return self

    async def parse(self, text: Optional[Text] = ""):
        """消息解析"""
        response = await self.agent.parse_message_using_nlu_interpreter(text)
        return response

    async def handle_text(self, text: Optional[Text] = "", sender_id: Optional[Text] = UserMessage.DEFAULT_SENDER_ID):
        """消息处理"""
        response = await self.agent.handle_text(text, sender_id=sender_id)
        return response

    def _load_endpoints(self, endpoints: Optional[Text] = None):
        """加载enpoints文件"""
        endpoints = AvailableEndpoints.read_endpoints(endpoints)
        broker = EventBroker.create(endpoints.event_broker)
        self.tracker_store = TrackerStore.create(
            endpoints.tracker_store, event_broker=broker
        )
        self.generator = endpoints.nlg
        self.action_endpoint = endpoints.action
        self.lock_store = LockStore.create(endpoints.lock_store)
