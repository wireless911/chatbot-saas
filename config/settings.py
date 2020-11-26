import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CONFIG PATH
CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))

# DEPLOY MODE
mode = os.environ.get("MODE")

# CHATBOT PATH
TRAIN_DATA_PATH = "/chatbot/"
MODEL_PATH = "models/"

# REDIS SUB RELOAD CHANNEL
PUB_ACTION = "reload_{mode}_bots"
SUB_ACTION = f"reload_{mode}_bots"

# REDIS
REDIS_URL = "redis://localhost"
REDIS_PASSWORD = 123456
SUB_ACTION_REDIS_PASS = dict(db=15, password=REDIS_PASSWORD)
CACHE_REDIS_PASS = dict(db=14, password=REDIS_PASSWORD)

# SANIC_JWT
# ACCESS_TOKEN_EXPIRE_TIME
EXPIRE_TIME = 60 * 30
# SCOPES
SCOPES_USER = ["user", "test", "admin"]
SCOPES_TEST = ["test", "admin"]
SCOPES_ADMIN = ["admin"]

# MYSQL
MYSQL_URL = "localhost"
PASSWORD = "glossa_address_parse"
MYSQL_PARAMS = dict(host=MYSQL_URL, user="root", password=PASSWORD, port=3306, max_connections=100, database="chatbot")
