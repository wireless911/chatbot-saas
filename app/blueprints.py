from sanic import Blueprint
from app.ai.blueprint import ai_bp
from app.bots.blueprint import bot_bp


# 路由分组
bp = Blueprint.group(ai_bp,bot_bp, url_prefix="/")
