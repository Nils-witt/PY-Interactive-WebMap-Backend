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
        model = event["model_type"]
        if model == MapGroup:
            instance = MapGroupSerializerWS(event['object'])
        elif model == MapStyle:
            instance = MapStyleSerializerWS(event['object'])
        elif model == MapOverlay:
            instance = MapOverlaySerializerWS(event['object'])
        elif model == NamedGeoReferencedItem:
            instance = NamedGeoReferencedItemSerializerWS(event['object'])
        else:
            instance = {'error': 'Unknown model type'}


        if self.user.has_perm(f'{model._meta.app_label}.view_{model._meta.model_name}'):
            self.send(text_data=json.dumps({
                'event': 'model.update',
                'model_type': model.__name__,
                'data': instance.data,
                'sender': 'system'
            }))

    def model_delete(self, event):
        model = event["model_type"]
        if self.user.has_perm(f'{model._meta.app_label}.view_{model._meta.model_name}'):
            self.send(text_data=json.dumps({
                'event': 'model.delete',
                'model_type': model.__name__,
                'object_id': str(event['object_id']),
                'sender': 'system'
            }))
