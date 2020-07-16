#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-management_v2 -> context
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/7/10 12:25
@Desc   ：
==================================================
"""

import os
import sys

from rasa.model import get_model

from config.settings import (TRAIN_DATA_PATH, MODEL_PATH)


class PathContext(object):
    """chatbot path 上下文"""

    def __init__(self, config):
        """
        :param config: {"bot_id":"wireless","version":"0.1"}
        """
        self.config = config
        self.version = config.get("version")
        self.bot_id = config.get("bot_id")

        self.chatbot_train_root_path = os.path.join(TRAIN_DATA_PATH, self.bot_id, self.version,self.bot_id,)
        self.chatbot_model_root_path = os.path.join(MODEL_PATH, self.bot_id, self.version)

        # train config
        self.config_file_path = os.path.join(self.chatbot_train_root_path, "config.yml")
        self.credentials_file_path = os.path.join(self.chatbot_train_root_path, "credentials.yml")
        self.endpoints_file_path = os.path.join(self.chatbot_train_root_path, "endpoints.yml")
        self.connect_path = os.path.join(self.chatbot_train_root_path, "channels.")
        self.domain_path = os.path.join(self.chatbot_train_root_path, "domain.yml")

        # train data
        self.nlu_md_path = os.path.join(self.chatbot_train_root_path, "nlu.md")
        self.stories_path = os.path.join(self.chatbot_train_root_path, "stories.md")

        # models
        # self.model_directory =get_model(MODEL_PATH)  # models 解压缩
        self.model_directory = self.chatbot_model_root_path  # models 解压缩

        # actions floder
        # self.action_package_path = "actions"
        self.action_package_path = os.path.join(TRAIN_DATA_PATH, "actions")
        # sys.path.insert(0,self.action_package_path)
