from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from objects.models import MapObject, MapGroup, MapOverlay, MapStyle, MapIcon


# Register your models here.


class MapObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'longitude', 'latitude', 'zoom')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at', 'groups')

    actions = ["set_zoom_18"]

    @admin.action()
    def set_zoom_18(self, request, queryset):
        queryset.update(zoom=18)


admin.site.register(MapObject, MapObjectAdmin)
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


class MapIconAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

    def icon(self, obj):
        return obj.icon.get('icon', {}).get('url', 'No Icon')


admin.site.register(MapIcon, MapIconAdmin)
