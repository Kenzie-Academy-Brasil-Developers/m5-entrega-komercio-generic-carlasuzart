
from products.models import Product
from products.permissions import ProductCustomPermission, SellerOwnerOrReadOnly
from products.serializers import GetProductsSerializer, ProductsSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class ProductsView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    
    permission_classes = [ProductCustomPermission]

    queryset = Product.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)

    serializer_map = {
        'GET': GetProductsSerializer,
        'POST': ProductsSerializer
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [SellerOwnerOrReadOnly]

    serializer_class = ProductsSerializer

    queryset= Product.objects.all()


