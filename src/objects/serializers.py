from rest_framework import serializers

from objects.models import MapObject, MapOverlay, MapStyle, MapIcon


class MapObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapObject
        fields = ['url', 'id', 'name', 'description', 'longitude', 'latitude', 'zoom']


class MapOverlaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapOverlay
        fields = ['url', 'id', 'name', 'description', 'url', 'type']


class MapStyleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapStyle
        fields = ['url', 'id', 'name', 'description', 'url']


class MapIconSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapIcon
        fields = ['url', 'id', 'name', 'latitude', 'longitude', "grundzeichen", "organisation", "fachaufgabe",
                  "einheit", "verwaltungsstufe", "funktion", "symbol", "text", "typ", "icon_name", "organisation_name",
                  "farbe"]
