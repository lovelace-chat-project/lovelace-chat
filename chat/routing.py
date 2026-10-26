from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/echo/', consumers.EchoConsumer.as_asgi()),
    path('ws/chat/<str:room>/', consumers.ChatConsumer.as_asgi()),
]