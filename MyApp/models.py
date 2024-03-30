# models.py
from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    discount_percentage = models.IntegerField(null=False, blank=False)
    rating = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    rating_count = models.IntegerField(null=False, blank=False)
    image_path = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.name