from django.test import TestCase
from products.models import Product
from accounts.models import Account


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = {
            "description": "Iphone",
            "price": 8900.00,
            "quantity": 10,
            "is_active": True
        }

        cls.user = {
            "username": "Leandro",
            "first_name": "Leandro",
            "last_name": "Pereira",
            "is_seller": True
        }

        cls.account = Account.objects.create_user(**cls.user)
        cls.product = Product.objects.create(
            **cls.product, seller=cls.account)

    def test_model_atributes(self):
        product = Product.objects.get(id=self.product.id)
        price_max_digits = product._meta.get_field("price").max_digits
        price_decimal = product._meta.get_field("price").decimal_places

        self.assertEqual(price_max_digits, 10)
        self.assertEqual(price_decimal, 2)


class RelationsProductsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = {
            "description": "Iphone",
            "price": 8900.00,
            "quantity": 10,
            
        }

        cls.user_1 = {
            "username": "Leandro",
            "first_name": "Leandro",
            "last_name": "Pereira",
            "is_seller": True
        }

        cls.user_2 = {
            "username": "Thiago",
            "first_name": "Thiago",
            "last_name": "Amorim",
            "is_seller": True
        }

        cls.data_1 = Account.objects.create_user(**cls.user_1)
        cls.data_2 = Account.objects.create_user(**cls.user_2)
        cls.product = Product.objects.create(
            **cls.product, seller=cls.data_1)

    def test_one_product_only_for_one_seller(self):
        self.assertIn(self.product, self.data_1.products.filter(
            description="Iphone"))

        self.data_2.products.add(self.product)
        self.assertNotIn(self.product, self.data_1.products.filter(
            description="Iphone"))
        self.assertIn(self.product, self.data_2.products.filter(
            description="Iphone"))