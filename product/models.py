from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class ProductImages(models.Model):
    image1 = models.ImageField(blank=True)
    image2 = models.ImageField(blank=True)
    image3 = models.ImageField(blank=True)
    image4 = models.ImageField(blank=True)
    image5 = models.ImageField(blank=True)


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    product_images = models.OneToOneField(ProductImages, on_delete=models.CASCADE,
                                       blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Product)
def create_profile(sender, instance, **kwargs):
    if not instance.product_images:
        product_images = ProductImages.objects.create()
        instance.product_images = product_images
