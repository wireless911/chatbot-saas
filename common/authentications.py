#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> authentications
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/10/26 11:40
@Desc   ：
==================================================
"""
from aioredis import Redis
from sanic.response import json
from sanic_jwt import exceptions, Authentication, Responses

from config.settings import EXPIRE_TIME
from models import dbManger
from models.model import UserModel
from sanic.log import logger as _logger


async def my_scope_extender(user, *args, **kwargs):
    return user.scopes


class MyAuthentication(Authentication):
    """自定义认证"""

    async def authenticate(self, request, *args, **kwargs):
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username or not password:
            raise exceptions.AuthenticationFailed("Missing username or password.")

        user = await dbManger.get(UserModel,username=username)

        if user is None:
            raise exceptions.AuthenticationFailed("User not found.")

        if password != user.password:
            raise exceptions.AuthenticationFailed("Password is incorrect.")

        return user

    async def store_refresh_token(
            self, user_id, refresh_token, *args, **kwargs
    ):
        key = "refresh_token_{user_id}".format(user_id=user_id)
        redis = self.app.redis  # type:Redis
        await redis.set(key, refresh_token)

    async def retrieve_refresh_token(self, user_id, *args, **kwargs):
        key = "refresh_token_{user_id}".format(user_id=user_id)
        redis = self.app.redis  # type:Redis
        token = await redis.get(key)
        return token

    async def retrieve_user(self, request, payload, *args, **kwargs):
        if payload:
            user_id = payload.get("user_id", None)
            return {"user_id": user_id}

        else:
            return None


class MyResponses(Responses):
    """自定义响应"""

    @staticmethod
    async def get_access_token_output(request, user, config, instance):
        access_token = await instance.auth.generate_access_token(user)

        output = {
            config.access_token_name(): access_token,
            "expire":EXPIRE_TIME
        }

        return access_token, output

