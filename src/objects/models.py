import uuid

from django.conf import settings
from django.db import models


# Create your models here.


class UUIDMixIn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampMixIn(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnerShipMixIn(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        abstract = True


class MapGroup(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, models.Model):
    """
    Base class for all map groups.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GeoReferencedMixin(models.Model):
    """
    Mixin for models that need geographic coordinates.
    """
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom_level = models.IntegerField(blank=True, null=True)
    show_on_map = models.BooleanField(default=False)
    group = models.ForeignKey(MapGroup, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        abstract = True


class MapStyle(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MapOverlay(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('raster', 'Raster'), ('vector', 'Vector')], default='raster')

    def __str__(self):
        return self.name


class NamedGeoReferencedItem(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, GeoReferencedMixin, models.Model):
    """
    Base class for items that have a name and geographic coordinates.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    symbol = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name
