from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers

from objects.models import MapOverlay, MapStyle, NamedGeoReferencedItem, MapGroup


class MapOverlaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapOverlay
        fields = ['url', 'id', 'name', 'description', 'url', 'type']


class MapStyleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapStyle
        fields = ['url', 'id', 'name', 'description', 'url']


class MapGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapGroup
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']

class NamedGeoReferencedItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NamedGeoReferencedItem
        fields = '__all__'