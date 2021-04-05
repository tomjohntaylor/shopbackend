from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return self.name
