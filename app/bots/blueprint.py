from sanic import Blueprint
from .views import BotsViews,BotViews


# 创建蓝图
bot_bp = Blueprint('/bots', url_prefix="/bots")

# 添加路由

bot_bp.add_route(BotsViews.as_view(), "/")
bot_bp.add_route(BotViews.as_view(), "/<id:int>")
