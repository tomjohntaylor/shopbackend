from django.urls import path
from product.api.views import *


urlpatterns = [
    path("products/",
         ProductListCreateAPIView.as_view(), 
         name="product-list"),

    path("products/<int:pk>/",
         ProductDetailAPIView.as_view(), 
         name="product-detail"),
]