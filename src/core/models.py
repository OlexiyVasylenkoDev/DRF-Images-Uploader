import os
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.utils.safestring import mark_safe

from core.utils.validators import validate_image_format, validate_image_size


class Thumbnail(models.Model):
    size = models.IntegerField(default=200)

    def __str__(self):
        return str(self.size)


class AccountTier(models.Model):
    title = models.CharField(max_length=128, default=None, null=True, blank=True)
    thumbnail_size = models.ManyToManyField(to="core.Thumbnail")
    original_link = models.BooleanField()
    expiring_link = models.BooleanField()

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    account_tier = models.ForeignKey(
        to=AccountTier, default=None, null=True, blank=True, on_delete=models.SET_NULL
    )


def set_unique_filename(instance, filename):
    ext = filename[len(filename) - 3:]
    unique_name = str(uuid4())
    filename = f'{unique_name}.{ext}'
    return os.path.join('', filename)


class Image(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, blank=False)
    file = models.ImageField(
        upload_to=set_unique_filename,
        validators=[
            validate_image_format, validate_image_size,
        ],
    )

    def img_preview(self):
        return mark_safe(f'<img src = "{self.file.url}" width = "100"/>')
