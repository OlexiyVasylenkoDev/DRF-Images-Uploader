from django.urls import reverse

from tests.base_test_setup import BaseTestSetup


class TestAuthentication(BaseTestSetup):

    def test_list_images(self):
        response = self.client.get(reverse("core:list-list"))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_list(self):
        self.client.logout()
        response = self.client.get(reverse("core:list-list"))
        self.assertEqual(response.status_code, 401)

    def test_upload_image(self):
        response = self.client.post(reverse("core:upload-list"), {'file': self.mock_image})
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_upload(self):
        self.client.logout()
        response = self.client.post(reverse("core:upload-list"), {'file': self.mock_image})
        self.assertEqual(response.status_code, 401)
