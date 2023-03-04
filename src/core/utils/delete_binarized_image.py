import os

from celery import shared_task

from config.settings import MEDIA_ROOT


@shared_task
def delete_image(img):
    os.remove(os.path.join(MEDIA_ROOT, img + ".png"))
    return "Deleted!"
