from channels.routing import ProtocolTypeRouter, URLRouter
from user_handler.ws_auth_middleware import TokenAuthMiddleware
import user_handler.routing


application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            user_handler.routing.websocket_urlpatterns
        )
    ),
})