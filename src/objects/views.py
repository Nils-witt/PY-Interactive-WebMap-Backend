from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.


def export_view(request):
    """
    View to handle export requests.
    """
    content_type = request.GET.get('ct')
    ids = request.GET.get('ids')
    all = request.GET.get('all', 'false').lower() == 'true'

    if not content_type:
        return render(request, 'error.html', {'message': 'Invalid parameters'})

    if all:
        objs = ContentType.objects.get_for_id(int(content_type)).get_all_objects_for_this_type()
        print(objs)
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", objs, stream=response)
        return response
    return render(request, 'export.html', {'content_type': content_type, 'ids': ids})