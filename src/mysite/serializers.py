from guardian.shortcuts import get_objects_for_user
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from objects.models import MapOverlay


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['overlays'] = []
        if user.is_superuser:
            for overlay in MapOverlay.objects.all():
                token['overlays'].append(overlay.permission_name)
        else:
            for overlay in get_objects_for_user(user, 'objects.view_mapoverlay'):
                token['overlays'].append(overlay.permission_name)


        return token
