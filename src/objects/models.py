import uuid

from asgiref.sync import async_to_sync
from auditlog.registry import auditlog
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from django.dispatch import receiver
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


auditlog.register(UnitStatus)


class UnitLocation(UUIDMixIn, TimeStampMixIn, models.Model):
    """
    Model representing the location history of a unit.
    """
    latitude = models.FloatField()
    longitude = models.FloatField()
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='location_history')

    def __str__(self):
        return f"Lat: {self.latitude}, Lon: {self.longitude}"


auditlog.register(UnitLocation)


class MapGroup(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, models.Model):
    """
    Base class for all map groups.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

@receiver([models.signals.post_save], sender=MapGroup)
def map_group_change_notify(sender, instance, **kwargs):
    if instance.pk:
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": type(instance), 'object_id': instance.pk})

auditlog.register(MapGroup)


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

@receiver([models.signals.post_save], sender=MapStyle)
def map_style_change_notify(sender, instance, **kwargs):
    if instance.pk:
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": "MapStyle", 'object_id': instance.pk.__str__()})


auditlog.register(MapStyle)


class MapOverlay(UUIDMixIn, TimeStampMixIn, OwnerShipMixIn, models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permission_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    type = models.CharField(max_length=50, choices=[('raster', 'Raster'), ('vector', 'Vector')], default='raster')
    file_structure = models.CharField(max_length=100)
    file_directory = models.CharField(max_length=255)
    file_base_url = models.CharField(max_length=255)
    def __str__(self):
        return self.name

@receiver([models.signals.post_save], sender=MapOverlay)
def map_overlay_change_notify(sender, instance, **kwargs):
    if instance.pk:
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": "MapOverlay", 'object_id': instance.pk.__str__()})


auditlog.register(MapOverlay)


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

@receiver([models.signals.post_save], sender=NamedGeoReferencedItem)
def named_geo_referenced_item_change_notify(sender, instance, **kwargs):
    if instance.pk:
        async_to_sync(channel_layer.group_send)("chat",
                                                {"type": "model.update", "model_type": "NamedGeoReferencedItem", 'object_id': instance.pk.__str__()})

auditlog.register(NamedGeoReferencedItem)


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


@receiver(models.signals.pre_save, sender=Unit)
def unit_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = Unit.objects.get(pk=instance.pk)
            if instance.unit_status != previous.unit_status:
                instance.unit_status_timestamp = now()
            if instance.latitude != previous.latitude or instance.longitude != previous.longitude:
                instance.location_timestamp = now()
        except:
            pass
    else:
        instance.unit_status_timestamp = now()
        instance.location_timestamp = now()

@receiver(models.signals.post_save, sender=Unit)
def unit_post_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous = Unit.objects.get(pk=instance.pk)
            if instance.unit_status != previous.unit_status:
                UnitStatus.objects.create(status=instance.unit_status, unit=instance)
            if instance.latitude != previous.latitude or instance.longitude != previous.longitude:
                UnitLocation.objects.create(latitude=instance.latitude, longitude=instance.longitude, unit=instance)
        except:
            UnitStatus.objects.create(status=instance.unit_status, unit=instance)
            UnitLocation.objects.create(latitude=instance.latitude, longitude=instance.longitude, unit=instance)
    async_to_sync(channel_layer.group_send)("chat",
                                            {"type": "model.update", "model_type": "Unit", 'object_id': instance.pk.__str__()})


auditlog.register(Unit)
