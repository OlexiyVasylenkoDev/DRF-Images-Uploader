from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from config.settings import MEDIA_URL, NGINX_PORT
from core.models import Image


class UploadImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "file"]


class ImageSerializer(ModelSerializer):
    photos = SerializerMethodField()

    def get_photos(self, obj):
        result = dict()
        for i in [j.size for j in obj.user.account_tier.thumbnail_size.all()]:
            result[f"Link_{i}"] = f"http://localhost:{NGINX_PORT}/{obj.file}/{i}"
        if obj.user.account_tier.original_link:
            result["Original_link"] = f"http://localhost:{NGINX_PORT}{MEDIA_URL}{obj.file}"
        if obj.user.account_tier.expiring_link:
            result["Expiring_link"] = f"http://localhost:{NGINX_PORT}/binary/{obj.file}/30"
        return result

    class Meta:
        model = Image
        fields = ["id", "user", "photos"]
