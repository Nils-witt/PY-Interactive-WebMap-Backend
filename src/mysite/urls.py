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
from django.urls import path, include
from rest_framework import viewsets, routers, permissions

import objects.views
from objects.models import MapObject, MapOverlay, MapStyle, MapIcon
from objects.serializers import MapObjectSerializer, MapOverlaySerializer, MapStyleSerializer, MapIconSerializer


class MapObjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = MapObject.objects.all()
    serializer_class = MapObjectSerializer


class MapOverlayViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = MapOverlay.objects.all()
    serializer_class = MapOverlaySerializer


class MapStyleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = MapStyle.objects.all()
    serializer_class = MapStyleSerializer


class MapIconViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = MapIcon.objects.all()
    serializer_class = MapIconSerializer


router = routers.DefaultRouter()
router.register(r'mapobjects', MapObjectViewSet)
router.register(r'overlays', MapOverlayViewSet)
router.register(r'styles', MapStyleViewSet)
router.register(r'map_items', MapIconViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('export/', objects.views.export_view),  # Assuming export_view is defined in objects.urls
]
