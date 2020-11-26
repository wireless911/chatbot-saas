from sanic import Blueprint
from app.ai.views import ModelTrainViews, ModelParseViews, ModelChatViews,ModelPublishViews


# 创建蓝图
ai_bp = Blueprint('/ai', url_prefix="/ai")

# 添加路由
ai_bp.add_route(ModelTrainViews.as_view(), "/train",stream=True)
ai_bp.add_route(ModelPublishViews.as_view(), "/publish")
ai_bp.add_route(ModelParseViews.as_view(), "/parse")
ai_bp.add_route(ModelChatViews.as_view(), "/chat")
