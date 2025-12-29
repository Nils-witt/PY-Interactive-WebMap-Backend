import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from django.utils.timezone import now

channel_layer = get_channel_layer()


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


class UnitStatus(UUIDMixIn, TimeStampMixIn, models.Model):
    """
    Model representing the status of a unit.
    """
    status = models.IntegerField()
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='status_history')

    def __str__(self):
        return self.status.__str__()


class UnitLocation(UUIDMixIn, TimeStampMixIn, models.Model):
    """
    Model representing the location history of a unit.
    """
    latitude = models.FloatField()
    longitude = models.FloatField()
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='location_history')

    def __str__(self):
        return f"Lat: {self.latitude}, Lon: {self.longitude}"


class MapGroup(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, models.Model):
    """
    Base class for all map groups.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": type(self), 'object': self})


class GeoReferencedMixin(models.Model):
    """
    Mixin for models that need geographic coordinates.
    """
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class MapStyle(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": type(self), 'object': self})


class MapOverlay(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permission_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    url = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('raster', 'Raster'), ('vector', 'Vector')], default='raster')

    def __str__(self):
        return self.name

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": type(self), 'object': self})


class NamedGeoReferencedItem(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, GeoReferencedMixin, models.Model):
    """
    Base class for items that have a name and geographic coordinates.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    zoom_level = models.IntegerField(blank=True, null=True)
    show_on_map = models.BooleanField(default=False)
    group = models.ForeignKey(MapGroup, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": type(self), 'object': self})


class Unit(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, GeoReferencedMixin, models.Model):
    """
    Model representing a unit of measurement.
    """
    name = models.CharField(max_length=100, unique=True)
    symbol = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    unit_status = models.IntegerField(blank=True, null=True)
    unit_status_timestamp = models.DateTimeField(blank=True, null=True)
    speak_request = models.BooleanField(default=False)
    route = models.JSONField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__unit_status_initial = self.unit_status
        self.__unit_status_timestamp = self.unit_status_timestamp
        self.__latitude_initial = self.latitude
        self.__longitude_initial = self.longitude

    def __str__(self):
        return self.name

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.unit_status_timestamp = self.__unit_status_timestamp
        status_changed = self.unit_status != self.__unit_status_initial
        location_changed = self.latitude != self.__latitude_initial or self.longitude != self.__longitude_initial
        if status_changed:
            self.unit_status_timestamp = now()
            self.__unit_status_initial = self.unit_status
        if location_changed:
            self.location_timestamp = now()
            self.__latitude_initial = self.latitude
            self.__longitude_initial = self.longitude

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if status_changed:
            UnitStatus.objects.create(status=self.unit_status, unit=self)
        if location_changed:
            UnitLocation.objects.create(latitude=self.latitude, longitude=self.longitude, unit=self)
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": type(self), 'object': self})
