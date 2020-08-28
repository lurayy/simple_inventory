from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.db import close_old_connections


@database_sync_to_async
def close_connection():
    close_old_connections()


@database_sync_to_async
def get_user(token):
    valid_data = VerifyJSONWebTokenSerializer().validate({'token':token})
    return valid_data['user']

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    see:
    https://channels.readthedocs.io/en/latest/topics/authentication.html#custom-authentication
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        await close_connection()
        token = parse_qs(self.scope["query_string"].decode("utf8"))["token"][0]
        try:
            self.scope['user'] = await get_user(token)
        except:
            self.scope['user'] = None
        inner = self.inner(self.scope)
        return await inner(receive, send) 


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))