#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-management_v2 -> main
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/7/9 11:42
@Desc   ：
==================================================
"""

# argparse
from argparse import ArgumentParser

from app.blueprints import bp
from config.settings import EXPIRE_TIME

parser = ArgumentParser(prog='opmis-plus')
parser.add_argument('--port', dest='port', type=int, default=8000, help="service port")
parser.add_argument('--debug', dest='debug', action="store_true", default=False)
parser.add_argument('--workers', dest='workers', type=int, default=1, help='instance number')
parser.add_argument('--mode', dest='mode', default="test", help='service mode')
options = parser.parse_args()
# 设置环境变量
import os

os.environ.setdefault("MODE", options.mode)

import multiprocessing
from sanic import Sanic
from config.log_conf import get_logging_config
from app.ai.blueprint import ai_bp
from app.bots.blueprint import bot_bp
from common.listeners import before_server_start, after_server_start
from sanic_openapi import swagger_blueprint
from sanic_jwt import initialize
from common.authentications import  MyAuthentication, MyResponses, my_scope_extender
from common.exceptions import server_error_handler, CustomErrorHandler


def config_swagger(app: Sanic) -> Sanic:
    """
    basic swagger config
    :param app: Sanic
    :return app: Sanic
    """
    app.config["API_HOST"] = "http://127.0.0.1:8000"
    app.config["API_BASEPATH"] = "/"
    app.config["API_SCHEMES"] = ["http"]
    app.config["API_VERSION"] = "0.1.0"
    app.config["API_TITLE"] = "chatbot-saas-api"
    app.config["API_DESCRIPTION"] = "chabot saas backend service"
    app.config["API_CONTACT_EMAIL"] = "lucas.hao@ibluesh.com"

    return app


def initialize_authentication(app: Sanic) -> Sanic:
    """
    initialize authentication
    :param app: Sanic
    :return app: Sanic
    """
    # initialize(app, authenticate=authenticate)
    initialize(
        app,
        authentication_class=MyAuthentication,
        responses_class=MyResponses,
        add_scopes_to_payload=my_scope_extender,
        scopes_enabled=True,
        expiration_delta=EXPIRE_TIME,
        refresh_token_enabled=True,
        claim_nbf=True,
        claim_nbf_delta=1, # 偏移量
        leeway=1 # 应用程序将用于解决系统时间配置中的细微变化的时间

    )
    return app


def config_app(app: Sanic) -> Sanic:
    """
    basic app config
    :param app: Sanic
    :return app: Sanic
    """
    # Initialize shared object of type unsigned int for tracking
    # the number of active training processes
    app.active_training_processes = multiprocessing.Value("I", 0)

    # app deploy
    app.mode = options.mode
    app.workers = options.workers

    # register blueprint
    app.blueprint(bp)
    app.blueprint(swagger_blueprint)

    # config swagger
    app = config_swagger(app)

    # register listener
    app.register_listener(before_server_start, 'before_server_start')
    app.register_listener(after_server_start, 'after_server_start')

    # register exception
    # app.error_handler.add(Exception, server_error_handler)

    app.error_handler = CustomErrorHandler()

    # jwt
    app = initialize_authentication(app)

    return app  # type: Sanic


def main():
    """Sanic main function"""
    app = Sanic(
        __name__,
        configure_logging=True,
        log_config=get_logging_config(f"{main.__name__}.{options.mode}")
    )  # type: Sanic
    app = config_app(app)  # type: Sanic
    app.run(host="0.0.0.0", port=options.port, workers=options.workers, auto_reload=False)


if __name__ == '__main__':
    main()
