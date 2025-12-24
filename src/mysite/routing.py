from django.urls import re_path

from .consumers import MyConsumer

websocket_urlpatterns = [
    re_path(r'api/ws/$', MyConsumer.as_asgi()),
]
