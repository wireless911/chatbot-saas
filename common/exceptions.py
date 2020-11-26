#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> exceptions
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/10/26 15:34
@Desc   ：
==================================================
"""
from sanic.response import json
from sanic.handlers import ErrorHandler
from sanic.log import logger as _logger
async def server_error_handler(request, exception):
    return json({"msg": "Oops, server error"}, status=500)




class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        ''' handles errors that have no error handlers assigned '''
        # You custom error handling logic...
        _logger.info(exception)
        return super().default(request, exception)