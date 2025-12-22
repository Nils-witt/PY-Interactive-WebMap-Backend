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
        fields = ['url', 'id', 'name', 'description']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login', 'first_name', 'last_name']


class NamedGeoReferencedItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NamedGeoReferencedItem
        fields = ['url', 'id', 'name', 'latitude', 'longitude', 'zoom_level', 'show_on_map', 'group', 'group_id',
                  'symbol', 'created_at', 'updated_at', 'description']
