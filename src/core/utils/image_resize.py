import cv2
from celery import shared_task

from config.settings import BASE_DIR, MEDIA_URL


@shared_task
def resize_image(filename, height):
    filename_to_save = str(BASE_DIR) + MEDIA_URL + filename
    img = cv2.imread(filename_to_save)
    height_width_ratio = img.shape[1] / img.shape[0]
    width = round(height * height_width_ratio)
    resized = cv2.resize(img, (width, height))
    resized_name = f"{filename_to_save[:len(filename_to_save) - 4]}_{height}.png"
    cv2.imwrite(resized_name, resized)
    return f"{filename[:len(filename) - 4]}_{height}.png"
