import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from objects.models import MapOverlay, MapGroup, NamedGeoReferencedItem, MapStyle
from objects.serializers import NamedGeoReferencedItemSerializerWS, MapGroupSerializerWS, MapStyleSerializerWS, \
    MapOverlaySerializerWS


class MyConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
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
        try:
            text_data_json = json.loads(text_data)
            command = text_data_json.get('command', '')
            if command.lower() == 'ping':
                self.send(text_data=json.dumps({
                    'message': 'pong',
                    'sender': 'system'
                }))
            if command.lower() == 'whoami':
                self.send(text_data=json.dumps({
                    'message': f'You are {self.user.get_username()}',
                    'sender': 'system'
                }))
            if command.lower() == 'model.update':
                self.model_update_received(text_data_json.get('model', None), text_data_json.get('id', None), text_data_json.get('data', None))
        except Exception as e:
            print(e)
            self.send(text_data=json.dumps({
                'message': 'Error processing message',
                'sender': 'system',
                'payload': text_data
            }))


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

    def model_update_received(self, model_name: str, object_id: str, data):
        self.send(text_data=json.dumps({
            'event': 'model.update.received',
            'model_type': model_name,
            'object_id': object_id,
            'data': data,
            'sender': 'system'
        }))

        if model_name == "NamedGeoReferencedItem":
            instance = NamedGeoReferencedItem.objects.get(id=object_id)
            if 'name' in data.keys():
                instance.name = data['name']
            if 'latitude' in data.keys():
                instance.latitude = data['latitude']
            if 'longitude' in data.keys():
                instance.longitude = data['longitude']
            if 'zoom_level' in data.keys():
                instance.zoom_level = data['zoom_level']
            if 'show_on_map' in data.keys():
                instance.show_on_map = data['show_on_map']
            if 'description' in data.keys():
                instance.description = data['description']
            instance.save()
        else:
            self.send(text_data=json.dumps({
                'event': 'model.update.error',
                'model_type': model_name,
                'object_id': object_id,
                'message': 'Unknown or unsupported model type',
                'sender': 'system'
            }))
