import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from objects.models import MapOverlay, MapGroup, NamedGeoReferencedItem, MapStyle
from objects.serializers import NamedGeoReferencedItemSerializerWS, MapGroupSerializerWS, MapStyleSerializerWS, \
    MapOverlaySerializerWS


class MyConsumer(WebsocketConsumer):
    def __init__(self, *args: Unused, **kwargs: Unused):
        super().__init__(args, kwargs)
        self.user = None

    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return
        self.accept()
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)

        if settings.DEBUG:
            self.send(text_data=json.dumps({
                'message': 'Welcome!',
                'channel': self.channel_name,
                'username': self.user.get_username(),
                'sender': 'system'
            }))
        else:
            self.send(text_data=json.dumps({
                'message': 'Welcome!',
                'username': self.user.get_username(),
                'sender': 'system'
            }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)

    def receive(self, text_data):
        pass

    def model_update(self, event):
        if event["model_type"] == MapGroup:
            instance = MapGroupSerializerWS(event['object'])
        elif event["model_type"] == MapStyle:
            instance = MapStyleSerializerWS(event['object'])
        elif event["model_type"] == MapOverlay:
            instance = MapOverlaySerializerWS(event['object'])
        elif event["model_type"] == NamedGeoReferencedItem:
            instance = NamedGeoReferencedItemSerializerWS(event['object'])
        else:
            instance = {'error': 'Unknown model type'}

        self.send(text_data=json.dumps({
            'model_type': event["model_type"].__name__,
            'data': instance.data,
            'sender': 'system'
        }))
