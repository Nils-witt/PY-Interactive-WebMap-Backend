from time import strftime, gmtime

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods
import os
import re
import zipfile

from .models import MapOverlay


# Create your views here.


def test(request):
    return HttpResponse("Hello World")


@require_http_methods(["GET", "POST"])
def upload_overlay(request):
    user = getattr(request, "user", None)
    if not (user and user.is_authenticated and user.is_staff):
        return HttpResponse("Forbidden: admin only", status=403)

    if request.method == "GET":
        overlays = MapOverlay.objects.all()
        return render(request, "upload_zip.html", {"overlays": overlays})

    # POST handling
    upload = request.FILES.get("zip")
    if not upload:
        return JsonResponse({"error": "No file part named 'zip' provided."}, status=400)

    # Determine overlay name
    overlay_id = request.POST.get("overlay_id", "").strip()
    overlay = MapOverlay.objects.get(id=overlay_id) if overlay_id else None
    if not overlay:
        return JsonResponse({"error": "Invalid or missing overlay_id."}, status=400)

    overlay_base = getattr(settings, "OVERLAY_DIR", None)
    if not overlay_base:
        return JsonResponse({"error": "Server not configured with OVERLAY_DIR."}, status=500)

    dir = overlay.id.__str__() + '_' + strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    overlay_dir = os.path.abspath(os.path.join(overlay_base, dir))
    os.makedirs(overlay_dir, exist_ok=True)

    # Save uploaded zip to the overlay directory
    zip_filename = os.path.basename(getattr(upload, "name", "overlay.zip"))
    zip_path = os.path.join(overlay_dir, zip_filename)

    try:
        with open(zip_path, "wb+") as dest:
            for chunk in upload.chunks():
                dest.write(chunk)

        # Extract safely to overlay_dir
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for member in zf.namelist():
                # Normalize member path and prevent zip-slip
                member_path = os.path.normpath(member)
                if member_path.startswith(".."):
                    return JsonResponse({"error": "Zip contains forbidden paths."}, status=400)

                target_path = os.path.abspath(os.path.join(overlay_dir, member_path))
                if not target_path.startswith(overlay_dir + os.sep) and target_path != overlay_dir:
                    return JsonResponse({"error": "Zip contains entries outside target directory."}, status=400)

                # Create directories as needed
                if member.endswith('/') or member.endswith('\\'):
                    os.makedirs(target_path, exist_ok=True)
                    continue

                parent_dir = os.path.dirname(target_path)
                if parent_dir and not os.path.exists(parent_dir):
                    os.makedirs(parent_dir, exist_ok=True)

                # Extract file
                with zf.open(member) as source, open(target_path, "wb") as target:
                    shutil_chunk = source.read()
                    target.write(shutil_chunk)

    except zipfile.BadZipFile:
        return JsonResponse({"error": "Uploaded file is not a valid zip."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)
    overlay.file_directory = dir
    overlay.save()
    return JsonResponse({"ok": True, "overlay": overlay.id, "zip_stored_as": zip_filename})
