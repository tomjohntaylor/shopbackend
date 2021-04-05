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
        read_only_fields = ('price_summarized',)
        depth = 1

    def validate_products_ids_and_qty(self, value):
        invalid_product_id_list = []
        if value:
            for product_id, qty in value.items():
                if not Product.objects.filter(pk=product_id).exists():
                    invalid_product_id_list.append(product_id)
                try:
                    if int(qty) <= 0:
                        raise serializers.ValidationError(
                            "One of products qty is zero or less!")
                except ValueError:
                    raise serializers.ValidationError(
                        "Product qty must be positive integer!")

            if invalid_product_id_list:
                raise serializers.ValidationError(
                    "Non existing products ids: {}!".format(', '.join(invalid_product_id_list)))
        else:
            raise serializers.ValidationError(
                "No products selected for order")
        return value
