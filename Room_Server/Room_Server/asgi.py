"""
ASGI config for Room_Server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app2 import routing
# from Room_Server.app2 import routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Room_Server.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
            # routing.websocket_urlpatterns
        )
    )
})
