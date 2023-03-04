import glob
import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from config.settings import BASE_DIR, MEDIA_ROOT
from core.models import Image


@receiver(pre_delete, sender=Image)
def delete_user_photos(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, f"{MEDIA_ROOT}/{instance.file}")
    photos_to_delete = glob.glob(file_path[:len(file_path) - 5] + "*", recursive=False)
    for photo in photos_to_delete:
        os.remove(photo)
