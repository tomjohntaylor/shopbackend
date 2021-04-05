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

    def validate_products_ids_and_qty(self, value):
        invalid_product_id_list = []
        if value:
            for product_id in value.keys():
                if not Product.objects.filter(pk=product_id).exists():
                    invalid_product_id_list.append(product_id)
            if invalid_product_id_list:
                raise serializers.ValidationError(
                    "Non existing products ids: {}".format(', '.join(invalid_product_id_list)))
        else:
            raise serializers.ValidationError(
                "No products selected for order")
        return value
