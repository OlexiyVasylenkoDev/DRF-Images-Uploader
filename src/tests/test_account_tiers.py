from core.models import Thumbnail
from tests.base_test_setup import BaseTestSetup


class TestAccountTiers(BaseTestSetup):

    def get_account_tier_options(self):
        options = [i.size for i in self.test_user.account_tier.thumbnail_size.all()]
        options.append(self.test_user.account_tier.original_link)
        options.append(self.test_user.account_tier.expiring_link)
        return options

    def test_basic_tier(self):
        self.assertEqual(self.get_account_tier_options(), [200, False, False])

    def test_premium_tier(self):
        premium_size = Thumbnail.objects.create(size=400)
        self.test_accounttier.thumbnail_size.add(premium_size)
        self.test_accounttier.original_link = True
        self.assertEqual(self.get_account_tier_options(), [200, 400, True, False])

    def test_enterprise_tier(self):
        premium_size = Thumbnail.objects.create(size=400)
        self.test_accounttier.thumbnail_size.add(premium_size)
        self.test_accounttier.original_link = True
        self.test_accounttier.expiring_link = True
        self.assertEqual(self.get_account_tier_options(), [200, 400, True, True])

    def test_custom_tier(self):
        premium_size = Thumbnail.objects.create(size=400)
        custom_size = Thumbnail.objects.create(size=600)
        self.test_accounttier.thumbnail_size.add(premium_size, custom_size)
        self.test_accounttier.original_link = True
        self.test_accounttier.expiring_link = True
        self.assertEqual(self.get_account_tier_options(), [200, 400, 600, True, True])
