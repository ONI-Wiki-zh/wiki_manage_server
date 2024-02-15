from channels.routing import ProtocolTypeRouter, URLRouter

from WikiModel.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # Explicitly set 'http' key using Django's ASGI application.
    'websocket': URLRouter(
        websocket_urlpatterns
    )
})
