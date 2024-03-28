from rest_framework import viewsets

from MyApp.models import Product
from MyApp.serializers import ProductSerializer


class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer