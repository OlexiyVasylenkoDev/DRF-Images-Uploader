import json

from django.urls import reverse

from core.utils import validators
from tests.base_test_setup import BaseTestSetup
from tests.samples import mock_image


class TestValidation(BaseTestSetup):
    def test_validate_image_format(self):
        response = self.client.post(reverse("core:upload-list"), {"file": mock_image(suffix=".jpeg")})
        response_to_file = json.loads(response.content.decode())["file"][0]
        self.assertEqual(response_to_file, validators.WRONG_FORMAT)
