from rest_framework.test import APITestCase

from tests.samples import (mock_image, sample_accounttier, sample_thumbnail,
                           sample_user)


class BaseTestSetup(APITestCase):
    def setUp(self) -> None:
        self.mock_image = mock_image()

        self.test_thumbnail = sample_thumbnail()
        self.test_accounttier = sample_accounttier()

        self.test_accounttier.thumbnail_size.add(self.test_thumbnail)

        self.test_user = sample_user(username="user",
                                     account_tier=self.test_accounttier,
                                     email="email@email.com",
                                     is_active=True,)
        self.client.force_login(self.test_user)

    def tearDown(self) -> None:
        self.test_thumbnail.delete()
        self.test_accounttier.delete()
        self.test_user.delete()
