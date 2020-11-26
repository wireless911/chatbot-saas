#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-saas -> migration
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/10/20 17:23
@Desc   ：
==================================================
"""
import re

from models.model import *
from models import model
import inspect

# 找出模块里所有的类名
def get_classes(arg):
    classes = []
    clsmembers = inspect.getmembers(arg, inspect.isclass)
    for (name, x) in clsmembers:
        if re.match(r"[a-zA-z]+Model",name):
            classes.append(x)
    return classes


def migrate():
    class_list = [UserModel,RobotModel,IntentModel,SentenceModel,FaqModel,RasaModel]
    for c in class_list:
        c.migrate()
        print(f"{c}:数据表创建")



if __name__ == '__main__':
    migrate()

