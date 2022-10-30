from rest_framework import serializers

from accounts.models import Account

from .models import Product

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'is_seller', 'date_joined', 'is_active', 'is_superuser']


class ProductsSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    class Meta:
        model = Product
        fields = "__all__"
        #read_only_fields = ["seller", "id"]

class GetProductsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["seller"]



        

