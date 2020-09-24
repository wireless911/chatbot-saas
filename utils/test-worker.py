#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> test-worker
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/9/15 10:14
@Desc   ：
==================================================
"""

import asyncio
import aioredis

from config.settings import SUB_ACTION_REDIS_PASS


async def reader(ch):
    while (await ch.wait_message()):
        msg = await ch.get_json()
        print("Got Message:", msg)


async def main():
    sub = await aioredis.create_redis("redis://localhost",**SUB_ACTION_REDIS_PASS)
    pub = await aioredis.create_redis("redis://localhost",**SUB_ACTION_REDIS_PASS)
    res = await sub.subscribe('chan:1')
    ch1 = res[0]

    tsk = asyncio.ensure_future(reader(ch1))

    res = await pub.publish_json('chan:1', ["Hello", "world"])
    res = await pub.publish_json('chan:1', ["Hello", "world"])
    assert res == 1

    await sub.unsubscribe('chan:1')
    await tsk
    sub.close()
    pub.close()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
