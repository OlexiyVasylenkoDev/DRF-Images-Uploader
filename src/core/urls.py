from django.urls import include, path
from rest_framework import routers

from core.views import (ListImages, UploadImages, create_binary_image,
                        create_resized_image, serve_binary_image)

app_name = "core"

router = routers.DefaultRouter()
router.register("list_images", ListImages, basename="list")
router.register("upload_images", UploadImages, basename="upload")

urlpatterns = (
    [
        path("", include(router.urls)),
        path("binary/<str:binary_name>.png", serve_binary_image, name="expiring_image"),
        path("binary/<str:url>/<int:seconds>/", create_binary_image, name="binarize"),
        path("<str:url>/<int:size>/", create_resized_image, name="resize"),
    ]
)
