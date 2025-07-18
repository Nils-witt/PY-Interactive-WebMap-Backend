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
from objects.models import MapOverlay, MapStyle, NamedGeoReferencedItem
from objects.serializers import MapOverlaySerializer, MapStyleSerializer, \
     NamedGeoReferencedItemSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

class MapOverlayViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = MapOverlay.objects.all()
    serializer_class = MapOverlaySerializer


class MapStyleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = MapStyle.objects.all()
    serializer_class = MapStyleSerializer


class NamedGeoReferencedItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = NamedGeoReferencedItem.objects.all()
    serializer_class = NamedGeoReferencedItemSerializer


router = routers.DefaultRouter()
router.register(r'overlays', MapOverlayViewSet)
router.register(r'styles', MapStyleViewSet)
router.register(r'items', NamedGeoReferencedItemViewSet)

urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
