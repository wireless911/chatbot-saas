# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# from peewee import Model, PrimaryKeyField, CharField, TextField
# from playhouse.pool import PooledMySQLDatabase
#
# from config.settings import DATABASES_NAME, DATABASE_SETTING_DICT
#
# db = PooledMySQLDatabase(DATABASES_NAME,**DATABASE_SETTING_DICT)
#
# db.connect()
#
#
# class AddressParseLogsModel(Model):
#     class Meta:
#         database = db
#         db_table = "address_parse_logs"
#
#     id = PrimaryKeyField()
#     company = CharField(max_length=255)
#     request = TextField()
#     response = TextField()
#
# sql = AddressParseLogsModel.select().where(AddressParseLogsModel.id == 1)
# res = db.execute(sql)
#
# print(res)
