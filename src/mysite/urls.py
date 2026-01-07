"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include
from guardian.shortcuts import get_objects_for_user
from rest_framework import viewsets, routers, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from mysite import settings
from objects import views
from objects.models import MapOverlay, MapStyle, NamedGeoReferencedItem, MapGroup, Unit
from objects.serializers import MapOverlaySerializer, MapStyleSerializer, \
    NamedGeoReferencedItemSerializer, MapGroupSerializer, UserSerializer, UnitSerializer


class HasApiPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        else:
            return False


class MapOverlayViewSet(viewsets.ModelViewSet):
    permission_classes = [HasApiPermissions]
    queryset = MapOverlay.objects.all()
    serializer_class = MapOverlaySerializer

    def get_queryset(self):
        query_set = get_objects_for_user(self.request.user, 'objects.view_mapoverlay')
        return query_set


class MapStyleViewSet(viewsets.ModelViewSet):
    permission_classes = [HasApiPermissions]
    queryset = MapStyle.objects.all()
    serializer_class = MapStyleSerializer

    def get_queryset(self):
        query_set = get_objects_for_user(self.request.user, 'objects.view_mapstyle')
        return query_set


class NamedGeoReferencedItemViewSet(viewsets.ModelViewSet):
    permission_classes = [HasApiPermissions]
    queryset = NamedGeoReferencedItem.objects.all()
    serializer_class = NamedGeoReferencedItemSerializer

    def get_queryset(self):
        query_set = get_objects_for_user(self.request.user, 'objects.view_namedgeoreferenceditem')
        return query_set

class UnitViewSet(viewsets.ModelViewSet):
    permission_classes = [HasApiPermissions]
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get_queryset(self):
        query_set = get_objects_for_user(self.request.user, 'objects.view_unit')
        return query_set

class MapGroupSerializerViewSet(viewsets.ModelViewSet):
    permission_classes = [HasApiPermissions]
    queryset = MapGroup.objects.all()
    serializer_class = MapGroupSerializer

    def get_queryset(self):
        query_set = get_objects_for_user(self.request.user, 'objects.view_mapgroup')
        return query_set


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [HasApiPermissions]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        query_set = get_objects_for_user(self.request.user, 'auth.view_user')
        return query_set


router = routers.DefaultRouter()
router.register(r'overlays', MapOverlayViewSet)
router.register(r'styles', MapStyleViewSet)
router.register(r'items', NamedGeoReferencedItemViewSet)
router.register(r'map_groups', MapGroupSerializerViewSet)
router.register(r'users', UserViewSet)
router.register(r'units', UnitViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/upload-overlay/', views.upload_overlay, name='upload_overlay'),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns.append(path('test/', views.test, name='test'))
