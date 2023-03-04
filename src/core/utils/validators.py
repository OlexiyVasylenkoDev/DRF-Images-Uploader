from django.core.exceptions import ValidationError

WRONG_FORMAT = "Sorry, image can be only of '.jpg' or '.png' format!"
WRONG_SIZE = "File size should not exceed 10 MB."


def validate_image_format(image):
    if not (str(image).endswith(".jpg") or str(image).endswith(".png")):
        raise ValidationError(WRONG_FORMAT)


def validate_image_size(image):
    if image.size > 10 * 1024 * 1024:  # 10 MB
        raise ValidationError(WRONG_SIZE)
