from rest_framework import serializers

from objects.models import MapOverlay, MapStyle, NamedGeoReferencedItem


class MapOverlaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapOverlay
        fields = ['url', 'id', 'name', 'description', 'url', 'type']


class MapStyleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapStyle
        fields = ['url', 'id', 'name', 'description', 'url']


class NamedGeoReferencedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamedGeoReferencedItem
        fields = '__all__'