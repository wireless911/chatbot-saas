#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> rabbit
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/9/15 16:47
@Desc   ：
==================================================
"""


from utils.rabbitmq import RabbitMQ

def main():
    rm = RabbitMQ()
    rm.consume(rm.callback)


if __name__ == '__main__':
    main()