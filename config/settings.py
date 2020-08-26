import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from typing import Optional, Text

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# # read config
# with open("config-test.yml", encoding="utf-8") as f:
#     config = yaml.load(f.read())
#
#
# # Database Settings
# DATABASE_SETTING = config.get("mysql").get("model")
# REDIS_SETTING = config.get("redis").get("model")
#
# # chatbot path
# TRAIN_DATA_PATH = config.get("chabot").get("TRAIN_DATA_PATH")
# MODEL_PATH = config.get("chabot").get("TRAIN_DATA_PATH")

print("seting file loading")

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))


class Config(object):

    @classmethod
    def load_config_yml(cls, mode: Optional[Text] = "test"):
        with open(CONFIG_PATH + f"/config-{mode}.yml", encoding="utf-8") as f:
            config = yaml.load(f.read())
        return cls(config)

    def __init__(self, config=None):
        self.mysql = config.get("mysql")
        self.redis = config.get("redis")
        self.chatbot = config.get("chatbot")


config = Config.load_config_yml()

DATABASE_SETTING = config.mysql
REDIS_SETTING = config.redis

TRAIN_DATA_PATH = config.chatbot.get("TRAIN_DATA_PATH")
MODEL_PATH = config.chatbot.get("MODEL_PATH")


MODE = "test"