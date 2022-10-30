
from django.test import TestCase
from accounts.models import Account


# Create your tests here.
class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account_data = {
            "username": "carla",
            "password": "abcd",
            "first_name": "carla",
            "last_name": "suzart",
            "is_seller": True
        }

        cls.account = Account.objects.create(**cls.account_data)

    def test_first_name_max_length(self):
        max_length = self.account._meta.get_field('first_name').max_length

        self.assertEqual(max_length, 50)

    def test_account_field(self):
        self.assertEqual(self.account.username, self.account_data['username'])
        self.assertEqual(self.account.password, self.account_data['password'])
        self.assertEqual(self.account.first_name, self.account_data['first_name'])
        self.assertEqual(self.account.last_name, self.account_data['last_name'])
        self.assertEqual(self.account.is_seller, self.account_data['is_seller'])
