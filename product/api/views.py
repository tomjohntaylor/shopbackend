from rest_framework import generics

from product.models import Product
from product.api.pagination import SmallSetPagination
from product.api.permissions import ReadOnly
from product.api.serializers import ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [ReadOnly]
    pagination_class = SmallSetPagination


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ReadOnly]
