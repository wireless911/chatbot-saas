#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> response
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/11/17 11:08
@Desc   ：
==================================================
"""
from functools import partial

from sanic.response import HTTPResponse
from sanic.compat import Header


try:
    from ujson import dumps as json_dumps
except ImportError:
    from json import dumps

    # This is done in order to ensure that the JSON response is
    # kept consistent across both ujson and inbuilt json usage.
    json_dumps = partial(dumps, separators=(",", ":"))


class Response(HTTPResponse):
    """自定义响应类"""

    def __init__(
            self,
            data=None,
            status=200,
            message=None,
            headers=None,
            content_type="application/json"
    ):
        self.content_type = content_type

        body = dict(code=status,msg=message, data=data)

        json_str = json_dumps(body, ensure_ascii=False)

        self.body = self._encode_body(json_str)

        self.status = status
        self.headers = Header(headers or {})
        self._cookies = None
