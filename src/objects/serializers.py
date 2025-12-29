from django.contrib.auth.models import User
from rest_framework import serializers

from objects.models import MapOverlay, MapStyle, NamedGeoReferencedItem, MapGroup, Unit


class MapOverlaySerializerWS(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapOverlay
        fields = ['id', 'name', 'description', 'url', 'type']


class MapOverlaySerializer(MapOverlaySerializerWS):
    class Meta:
        model = MapOverlay
        fields = MapOverlaySerializerWS.Meta.fields + ['url']


class MapStyleSerializerWS(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapStyle
        fields = ['id', 'name', 'description', 'url']


class MapStyleSerializer(MapStyleSerializerWS):
    class Meta:
        model = MapStyle
        fields = MapStyleSerializerWS.Meta.fields + ['url']


class MapGroupSerializerWS(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapGroup
        fields = ['id', 'name', 'description']


class MapGroupSerializer(MapGroupSerializerWS):
    class Meta:
        model = MapGroup
        fields = MapGroupSerializerWS.Meta.fields + ['url']


class UserSerializerWS(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login',
                  'first_name', 'last_name']


class UserSerializer(UserSerializerWS):
    class Meta:
        model = User
        fields = UserSerializerWS.Meta.fields + ['url']


class NamedGeoReferencedItemSerializerWS(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NamedGeoReferencedItem
        fields = ['id', 'name', 'latitude', 'longitude', 'zoom_level', 'show_on_map', 'group', 'group_id',
                  'created_at', 'updated_at', 'description']


class NamedGeoReferencedItemSerializer(NamedGeoReferencedItemSerializerWS):
    class Meta:
        model = NamedGeoReferencedItem
        fields = NamedGeoReferencedItemSerializerWS.Meta.fields + ['url']


class UnitWS(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'latitude', 'longitude', 'unit_status', 'unit_status_timestamp', 'speak_request',
                  'symbol', 'created_at', 'updated_at', 'description', 'location_timestamp', 'route']


class UnitSerializer(UnitWS):
    class Meta:
        model = Unit
        fields = UnitWS.Meta.fields + ['url']
