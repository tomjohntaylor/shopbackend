from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from product.models import Product


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Order(models.Model):
    billing_address = models.TextField()
    delivery_address = models.TextField()
    products_ids_and_qty = models.JSONField(default=dict)
    price_summarized = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return self.order_nr


@receiver(pre_save, sender=Order)
def order_price_summarize(sender, instance, **kwargs):
    products_in_order = [Product.objects.get(id=product_id) for product_id in instance.products_ids_and_qty.keys()]
    instance.price_summarized = sum([product.price for product in products_in_order])
