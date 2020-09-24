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
from app.bots.blueprint import bots_bp
from common.listeners import before_server_start, after_server_start
from sanic_openapi import swagger_blueprint


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
    app.blueprint(bots_bp)
    app.blueprint(swagger_blueprint)

    # config swagger
    app = config_swagger(app)

    # register listener
    app.register_listener(before_server_start, 'before_server_start')
    app.register_listener(after_server_start, 'after_server_start')

    return app  # type: Sanic


def main():
    """Sanic main function"""

    app = Sanic(__name__, configure_logging=True,
                log_config=get_logging_config(f"{main.__name__}.{options.mode}"))  # type: Sanic
    app = config_app(app)  # type: Sanic
    app.run(host="0.0.0.0", port=options.port, workers=options.workers, auto_reload=True)


if __name__ == '__main__':
    main()
