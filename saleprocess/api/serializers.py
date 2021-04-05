from rest_framework import serializers
from saleprocess.models import Profile, Order
from product.models import Product

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ('profile',)
        depth = 1
