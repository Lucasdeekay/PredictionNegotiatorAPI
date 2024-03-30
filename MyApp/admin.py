from django.contrib import admin

from MyApp.models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'actual_price', 'discounted_price', 'discount_percentage', 'rating', 'rating_count', 'image_path')


admin.site.register(Product, ProductAdmin)
