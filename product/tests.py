from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from product.models import Product


class ProductViewsTest(APITestCase):
    current_profile_detail_url = reverse("product-list")

    # unauthorized user can view product list
    def test_if_unauthorized_user_can_view_product_list(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.current_profile_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 0)
        self.product1 = Product.objects.create(name="Samson",
                                               description="very-strong-password",
                                               price=999.99)
        self.product2 = Product.objects.create(name="Xiajuma",
                                               description="very-strong-password",
                                               price=1)
        response = self.client.get(self.current_profile_detail_url)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results'][0]['name'], 'Samson')
