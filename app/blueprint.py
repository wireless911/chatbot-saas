from sanic import Blueprint
from app.model import ModelTrainViews, ModelParseViews, ModelChatViews


# 创建蓝图
bp = Blueprint('/models', url_prefix="/models")

# 添加路由
bp.add_route(ModelTrainViews.as_view(), "/train",stream=True)
bp.add_route(ModelParseViews.as_view(), "/parse")
bp.add_route(ModelChatViews.as_view(), "/chat")
