import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from saleprocess.models import Profile, Order
from product.models import Product



class ProfileCreationAndViewTest(APITestCase):
    current_profile_detail_url = reverse("current-profile-detail")

    def setUp(self):
        self.user = User.objects.create_user(username="randomuser",
                                             password="very-strong-password")

    # after user creation connected profile is created automatically
    def test_user_profile_is_created_automatically(self):
        self.assertTrue(Profile.objects.filter(user=self.user))

    # unauthorized user cant view current profile (403)
    def test_if_unauthorized_user_cant_view_current_profile(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.current_profile_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # authorized user can view current profile (200) and it's his profile (assertEqual)
    def test_if_authorized_user_can_view_current_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.current_profile_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Profile.objects.get(id=response.json()['id']), Profile.objects.get(user=self.user))


class OrderOperationsTest(APITestCase):
    current_profile_detail_url = reverse("current-profile-detail")
    current_profile_order_list_url = reverse("current-profile-order-list")
    # current_profile_order_detail_url = reverse("current-profile-order-detail", kwargs={"pk": x})

    def setUp(self):
        self.user1 = User.objects.create_user(username="randomuser1",
                                              password="very-strong-password")
        self.user2 = User.objects.create_user(username="randomuser2",
                                              password="very-strong-password")
        self.product1 = Product.objects.create(name="Samson",
                                                    description="very-strong-password",
                                                    price=999.99)
        self.product2 = Product.objects.create(name="Xiajuma",
                                                    description="very-strong-password",
                                                    price=1)

    # unauthorized user can't create new order (403)
    def test_if_unauthorized_user_cant_create_new_order(self):
        self.client.force_authenticate(user=None)
        data = {"1": "0"}
        response = self.client.post(self.current_profile_order_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # authorized user can create new order (200) and it's his order
    def test_if_authorized_user_can_create_new_order(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "billing_address": "Some address",
            "delivery_address": "Some address",
            "products_ids_and_qty": "{\"1\": \"1\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.get(id=response.json()['id']).profile, Profile.objects.get(user=self.user1))
        data = {
            "billing_address": "Some other address",
            "delivery_address": "Some other address",
            "products_ids_and_qty": "{\"2\": \"1\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        self.assertEqual(len(Order.objects.filter(profile=Profile.objects.get(user=self.user1))), 2)

    # authorized user can't create order passing product id that doesnt exist
    def test_if_authorized_user_cant_create_order_if_passing_non_existing_product(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "billing_address": "Some address",
            "delivery_address": "Some address",
            "products_ids_and_qty": "{\"3\": \"1\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # authorized user can't create order passing product qty less or equal zero
    def test_if_authorized_user_cant_create_order_if_passing_non_positive_integer_as_qty(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "billing_address": "Some address",
            "delivery_address": "Some address",
            "products_ids_and_qty": "{\"1\": \"0\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {
            "billing_address": "Some address",
            "delivery_address": "Some address",
            "products_ids_and_qty": "{\"1\": \"asd\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # authorized user can view current profile orders (200) and it's there orders he created just before
    def test_if_authorized_user_can_view_his_orders_list(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "billing_address": "Some address",
            "delivery_address": "Some address",
            "products_ids_and_qty": "{\"1\": \"1\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.get(id=response.json()['id']).profile, Profile.objects.get(user=self.user1))
        data = {
            "billing_address": "Some other address",
            "delivery_address": "Some other address",
            "products_ids_and_qty": "{\"2\": \"1\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        response = self.client.get(self.current_profile_order_list_url)
        response_orders_id_list = [ord['id'] for ord in response.json()]
        orders_list = list(Order.objects.filter(profile=Profile.objects.get(user=self.user1)))
        response_orders_list = [Order.objects.get(id=id) for id in response_orders_id_list]
        self.assertEqual(response_orders_list, response_orders_list)

    # unauthorized user can't see details of order (403)
    def test_if_unauthorized_user_cant_see_orders_and_details_of_order(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "billing_address": "Some other address",
            "delivery_address": "Some other address",
            "products_ids_and_qty": "{\"2\": \"1\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        self.client.force_authenticate(user=None)
        response = self.client.get(self.current_profile_order_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(reverse("current-profile-order-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # other user cant see others orders on order (403)
    def test_if_other_user_cant_see_details_of_others_user_order(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "billing_address": "Some other address",
            "delivery_address": "Some other address",
            "products_ids_and_qty": "{\"2\": \"1\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse("current-profile-order-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # authorized user can see details of order he created (200) and summarized price is counted
    def test_if_authorized_user_can_see_details_of_his_order_with_summarized_prices_counted(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "billing_address": "Some other address",
            "delivery_address": "Some other address",
            "products_ids_and_qty": "{\"1\": \"1\", \"2\": \"1\"}"
        }
        response = self.client.post(self.current_profile_order_list_url, data)
        response = self.client.get(reverse("current-profile-order-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['billing_address'], response.json()['billing_address'])
        summarized_price_expected = sum([product.price for product in Product.objects.all()])
        self.assertEqual(str(summarized_price_expected), response.json()['price_summarized'])

# TODO: authorized user can delete an order he created (20X?) and on the order list there is only one order left
# TODO: authorized user can edit an order he created (20X?) and summarized price has changed


# TODO: unauthorized user can view product list and can only do get request
# TODO: unauthorized user can view product detail and can only do get request
