import cv2
from celery import shared_task

from config.settings import BASE_DIR, MEDIA_URL


@shared_task
def binarize_image(filename, binary_name):
    filename = str(BASE_DIR) + MEDIA_URL + filename
    img = cv2.imread(filename)
    greyscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(greyscale_img, 127, 255, cv2.THRESH_BINARY, )
    resized_name = f"{str(BASE_DIR) + MEDIA_URL + str(binary_name)}.png"
    print(resized_name)
    cv2.imwrite(resized_name, binary_img)
    return str(binary_name)
