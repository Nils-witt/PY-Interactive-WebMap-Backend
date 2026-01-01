from auditlog.mixins import AuditlogHistoryAdminMixin
from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from guardian.admin import GuardedModelAdmin

from objects.models import MapGroup, MapOverlay, MapStyle, NamedGeoReferencedItem, Unit, UnitStatus

# Register your models here.

admin.site.register(MapGroup)


class MapOverlayAdmin(GuardedModelAdmin):
    list_display = ('name', 'description', 'url', 'type')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

    actions = ["export_all_objects"]

    def export_all_objects(modeladmin, request, queryset):
        # elected = queryset.values_list("pk", flat=True)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect(
            "/export/?ct=%s&all=true"
            % (
                ct.pk
            )
        )


admin.site.register(MapOverlay, MapOverlayAdmin)


class MapStyleAdmin(GuardedModelAdmin):
    list_display = ('name', 'description', 'url')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

    actions = ["export_selected_objects"]

    def export_selected_objects(modeladmin, request, queryset):
        selected = queryset.values_list("pk", flat=True)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect(
            "/export/?ct=%s&ids=%s"
            % (
                ct.pk,
                ",".join(str(pk) for pk in selected),
            )
        )


admin.site.register(MapStyle, MapStyleAdmin)


class XForm(ActionForm):
    zoom_level = forms.IntegerField(required=False)


class NamedGeoReferencedItemAdmin(GuardedModelAdmin):
    list_display = ('name', 'longitude', 'latitude', 'zoom_level', 'show_on_map', 'group', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at', 'group', 'show_on_map', 'zoom_level')

    action_form = XForm
    actions = ["set_zoom_level"]

    def set_zoom_level(self, request, queryset):
        zoom_level = request.POST['zoom_level']
        print(zoom_level)
        if zoom_level is not None:
            queryset.update(zoom_level=zoom_level)
            self.message_user(request, f"Zoom level set to {zoom_level} for selected items.")


admin.site.register(NamedGeoReferencedItem, NamedGeoReferencedItemAdmin)


class UnitAdmin(GuardedModelAdmin):
    list_display = ('name', 'unit_status','unit_status_timestamp', 'longitude', 'latitude', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at', 'unit_status')


admin.site.register(Unit, UnitAdmin)


class UnitStatusAdmin(AuditlogHistoryAdminMixin,GuardedModelAdmin):
    show_auditlog_history_link = True
    list_display = ('status', 'unit', 'created_at')
admin.site.register(UnitStatus, UnitStatusAdmin)
