import tempfile

from PIL import Image

from core.utils.image_resize import resize_image
from tests.base_test_setup import BaseTestSetup


class TestChangingImages(BaseTestSetup):
    def test_resizing(self):
        test_image = Image.new("RGB", (150, 150), (225, 100, 30))
        file = tempfile.NamedTemporaryFile(suffix=".jpg")
        test_image.save(file)
        file.seek(0)
        resize_image(str(file), 200)
