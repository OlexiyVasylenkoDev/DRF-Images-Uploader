import tempfile

from django.contrib.auth import get_user_model
from PIL import Image

from core.models import AccountTier, Thumbnail


def sample_user(**params):
    defaults = {
        "is_staff": False,
    }
    defaults.update(**params)
    return get_user_model().objects.create(**defaults)


def sample_thumbnail(**params):
    defaults = {
        "size": 200,
    }
    defaults.update(**params)
    return Thumbnail.objects.create(**defaults)


def sample_accounttier(**params):
    defaults = {
        "title": "Basic",
        "original_link": False,
        "expiring_link": False,
    }
    defaults.update(**params)
    return AccountTier.objects.create(**defaults)


def mock_image(suffix='.png'):
    test_image = Image.new("RGB", (150, 150), (225, 100, 30))
    file = tempfile.NamedTemporaryFile(suffix=suffix)
    test_image.save(file)
    file.seek(0)
    return file
