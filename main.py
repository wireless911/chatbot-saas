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

import asyncio
import multiprocessing

from sanic import Sanic

from common.exception import CustomErrorHandler
from config.log_conf import get_logging_config
from app.blueprint import bp
from common.listeners import before_server_start


def config_app(app: Sanic) -> Sanic:


    # Initialize shared object of type unsigned int for tracking
    # the number of active training processes
    app.active_training_processes = multiprocessing.Value("I", 0)

    app.register_listener(before_server_start, 'before_server_start')

    # register blueprint
    app.blueprint(bp)

    return app  # type: Sanic


def main():
    """Sanic main function"""
    app = Sanic(__name__, configure_logging=True, log_config=get_logging_config(main.__name__))  # type: Sanic
    app = config_app(app)  # type: Sanic
    app.run(host="0.0.0.0", port=8080,workers=4)


if __name__ == '__main__':
    main()
