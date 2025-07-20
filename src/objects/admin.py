from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from objects.models import MapGroup, MapOverlay, MapStyle, NamedGeoReferencedItem
from django.contrib.admin.helpers import ActionForm
from django import forms

# Register your models here.

admin.site.register(MapGroup)


class MapOverlayAdmin(admin.ModelAdmin):
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


class MapStyleAdmin(admin.ModelAdmin):
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


class NamedGeoReferencedItemAdmin(admin.ModelAdmin):
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
