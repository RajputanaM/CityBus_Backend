
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from bus.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "http" : get_asgi_application() ,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
            ]
        )
    ),
})
