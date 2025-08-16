from django.http import HttpResponse


# Create your views here.


def test(request):
    print(request.user.has_perm('objects.view_mapoverlay'))
    return HttpResponse("Hello World")