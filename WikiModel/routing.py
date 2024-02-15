from django.urls import path, re_path
from WikiModel.views_websocket import PageStatusConsumer

websocket_urlpatterns = [
    # 前端请求websocket连接
    re_path(r'^pullPageStatus', PageStatusConsumer.as_asgi()),  # 拉取页面状态
]
