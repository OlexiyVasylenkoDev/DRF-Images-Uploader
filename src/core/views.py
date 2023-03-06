import os
import time
from uuid import uuid4

from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect
# Create your views here.
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config.settings import ALLOWED_HOSTS, MEDIA_ROOT, MEDIA_URL, NGINX_PORT
from core.models import Image
from core.serializers import ImageSerializer, UploadImageSerializer
from core.utils.delete_binarized_image import delete_image
from core.utils.image_binarize import binarize_image
from core.utils.image_resize import resize_image


class UploadImages(ModelViewSet):
    queryset = ""
    serializer_class = UploadImageSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    allowed_methods = ["POST"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListImages(ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ["GET"]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


def create_resized_image(request, url: str, size: int):
    allowed_sizes = [i.size for i in request.user.account_tier.thumbnail_size.all()]
    if not os.path.exists(MEDIA_ROOT + f"/{url[:len(url) - 4]}_{size}.png") and size in allowed_sizes:
        image_url = f"http://{ALLOWED_HOSTS[0]}:{NGINX_PORT}{MEDIA_URL}{resize_image(url, size)}"
    elif size not in allowed_sizes:
        return HttpResponseNotAllowed("Sorry!")
    else:
        image_url = f"http://{ALLOWED_HOSTS[0]}:{NGINX_PORT}{MEDIA_URL}{url[:len(url) - 4]}_{size}.png"
    return HttpResponseRedirect(image_url)


def create_binary_image(request, url: str, seconds: int):
    allowed_seconds = range(300, 30000)
    if seconds not in allowed_seconds:
        return HttpResponseNotAllowed("Sorry!")
    binary_name = uuid4()
    binarize_image.delay(url, binary_name)
    request.session["expiration_time"] = time.time() + seconds
    delete_image.apply_async(args=[binary_name], countdown=seconds)
    image_url = f"http://{ALLOWED_HOSTS[0]}:{NGINX_PORT}{MEDIA_URL}{str(binary_name)}.png"
    return HttpResponseRedirect(image_url)


def serve_binary_image(request, binary_name):
    image_url = f"http://{ALLOWED_HOSTS[0]}:{NGINX_PORT}{MEDIA_URL}{binary_name}.png"
    if time.time() > request.session["expiration_time"]:
        raise Http404("Image not found")
    return HttpResponseRedirect(image_url)
