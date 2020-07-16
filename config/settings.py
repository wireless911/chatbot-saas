import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODE = "test"

TRAIN_DATA_PATH = "/chatbot/train/"
MODEL_PATH = "/chatbot/model/"

# Database Settings
DATABASE_SETTING = {
    # "test": dict(database='chatbot', user="root", host="192.168.213.128", password="123456",
    #              port=3306, max_connections=100),
    "test": dict(database='chatbot', user="root", host="localhost", password="glossa_address_parse",
                 port=3306, max_connections=100),
    "product": dict(database='address_parse', user="root", host="mysql_service", password="glossa_address_parse",
                    port=3306, max_connections=100)
}.get(MODE)



