# models.py
from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    price = models.DecimalField(null=False, blank=False)
    rating = models.DecimalField(null=False, blank=False)
    upload_date = models.DateField(default=timezone.now().date(), null=False, blank=False)

    def __str__(self):
        return self.name