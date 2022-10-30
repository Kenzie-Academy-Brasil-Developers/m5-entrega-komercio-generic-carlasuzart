
from products.models import Product
from accounts.models import Account
from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token

# Create your tests here.

class ProductModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.url = '/api/products/'

        cls.product_data_1 = {
            "description": "Celular",
            "price": 3500,
            "quantity": 20,
        }

        cls.product_data_2 = {
            "description": "TV",
            "price": 4700,
            "quantity": 10,
        }

        cls.account_adm = {
            'username': 'admin',
            'password': 'admin123',
            'first_name': 'Carlos',
            'last_name':'Silva'
        }

        cls.account_is_seller_1 = {
            'username': 'seller',
            'password': 'seller123',
            'first_name': 'Joao',
            'last_name':'Silva',
            'is_seller': True
        }

        cls.account_is_seller_2 = {
            'username': 'seller2',
            'password': 'seller123',
            'first_name': 'Marina',
            'last_name':'Silva',
            'is_seller': True
        }

        cls.account_common = {
            'username': 'user',
            'password': 'user123',
            'first_name': 'Simone',
            'last_name':'Silva',
            'is_seller': False
        }

        cls.account_login_is_seller_1 = {
            "username":'seller',
            'password': 'seller123'
        }

        cls.account_login_is_seller_2 = {
            'username': 'seller2',
            'password': 'seller123'
        }

        cls.admin = Account.objects.create_superuser(**cls.account_adm)
        cls.token_admin = Token.objects.create(user=cls.admin)

        cls.is_seller_1 = Account.objects.create_user(**cls.account_is_seller_1)
        cls.token_is_seller_1 = Token.objects.create(user=cls.is_seller_1)

        cls.is_seller_2 = Account.objects.create_user(**cls.account_is_seller_2)
        cls.token_is_seller_2 = Token.objects.create(user=cls.is_seller_2)

        cls.common = Account.objects.create_user(**cls.account_common)
        cls.token_common = Token.objects.create(user=cls.common)

        cls.product_created = Product.objects.create(
            **cls.product_data_2, seller=cls.is_seller_2)

        cls.products = [
            Product.objects.create(
                description=f"Produto {product_id}",
                price=99,
                quantity=5,
                seller=cls.is_seller_1,
            )
            for product_id in range(1, 5)
        ]

    def test_create_product_with_seller(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_is_seller_1.key)

        response = self.client.post(
            self.url, data=self.product_data_1)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(len(response.data.keys()), 6)
        self.assertIn('id', response.data)
        self.assertIn("description",  response.data)
        self.assertIn("price",  response.data)
        self.assertIn("quantity",  response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("seller", response.data)

        self.assertEqual(len(response.data["seller"].keys()), 8)

    def test_create_product_without_token(self):
        response = self.client.post(
            self.url, data=self.product_data_1)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    


