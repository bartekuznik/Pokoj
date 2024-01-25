from django.urls import path
from . import game

websocket_urlpatterns = [
    path('ws/socket-server', game.GameConsumer.as_asgi())
]