
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
                price=1300,
                quantity=6,
                seller=cls.is_seller_1,
            )
            for product_id in range(1, 6)
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

    def test_create_product_with_not_seller(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_common.key)

        response = self.client.post(
            self.url, data=self.product_data_1)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["detail"], "You do not have permission to perform this action."
        )

    def test_create_product_with_adm(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.post(
            self.url, data=self.product_data_1)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["detail"], "You do not have permission to perform this action."
        )

    def test_create_with_wrong_keys(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_is_seller_1.key)

        response = self.client.post(
            self.url, data={})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["description"][0], "This field is required."
        )
        self.assertEqual(
            response.data["price"][0], "This field is required."
        )
        self.assertEqual(
            response.data["quantity"][0], "This field is required."
        )

    def test_can_filter_product(self):
        response = self.client.get(
            f'{self.url}{self.product_created.id}/')

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(len(response.data.keys()), 6)

    def test_only_owner_can_edit_product(self):
        product = Product.objects.create(**self.product_data_1, seller=self.is_seller_1)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_is_seller_1.key)

        response = self.client.patch(
            f'{self.url}{product.id}/', data={"price": 1200})

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(len(response.data.keys()), 6)

    def test_other_user_can_edit_product(self):
        product = Product.objects.create(**self.product_data_1, seller=self.is_seller_1)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_is_seller_2.key)

        response = self.client.patch(
            f'{self.url}{product.id}/', data={"price": 1200})

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_can_register_with_negative_number(self):
        product_data = {"description": "Iphone",
                        "price": 8900,
                        "quantity": -30, }

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_is_seller_2.key)

        response = self.client.post(
            self.url, data=product_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn("quantity", response.data)
        self.assertIn(
            "Ensure this value is greater than or equal to 0.", response.data["quantity"])




