from sanic import Blueprint
from app.bots.views import ModelTrainViews, ModelParseViews, ModelChatViews,ModelPublishViews


# 创建蓝图
bots_bp = Blueprint('/bots', url_prefix="/bots")

# 添加路由
bots_bp.add_route(ModelTrainViews.as_view(), "/train",stream=True)
bots_bp.add_route(ModelPublishViews.as_view(), "/publish")
bots_bp.add_route(ModelParseViews.as_view(), "/parse")
bots_bp.add_route(ModelChatViews.as_view(), "/chat")
