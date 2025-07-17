import uuid

from django.conf import settings
from django.db import models

from objects.takzeichen_types import get_grundzeichen_types, get_organisation_types, \
    get_fachaufgaben_types, get_einheits_types, get_verwaltungsstufen_types, get_funktion_types, get_symbol_types


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


class GeoReferencedMixin(models.Model):
    """
    Mixin for models that need geographic coordinates.
    """
    latitude = models.FloatField()
    longitude = models.FloatField()

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


class MapObject(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, GeoReferencedMixin, models.Model):
    """
    Base class for all map objects.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(MapGroup, blank=True, related_name='mapobjects')
    zoom = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


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


class MapIcon(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, GeoReferencedMixin, models.Model):
    name = models.CharField(max_length=100)

    grundzeichen = models.CharField(max_length=100, choices=get_grundzeichen_types, blank=True, null=True)
    organisation = models.CharField(max_length=100, choices=get_organisation_types, blank=True, null=True)
    fachaufgabe = models.CharField(max_length=100, choices=get_fachaufgaben_types, blank=True, null=True)
    einheit = models.CharField(max_length=100, choices=get_einheits_types, blank=True, null=True)
    verwaltungsstufe = models.CharField(max_length=100, choices=get_verwaltungsstufen_types, blank=True, null=True)
    funktion = models.CharField(max_length=100, choices=get_funktion_types, blank=True, null=True)
    symbol = models.CharField(max_length=100, choices=get_symbol_types, blank=True, null=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    typ = models.CharField(max_length=100, blank=True, null=True)
    icon_name = models.CharField(max_length=100, blank=True, null=True)
    organisation_name = models.CharField(max_length=100, blank=True, null=True)
    farbe = models.CharField(max_length=100, blank=True, null=True)
