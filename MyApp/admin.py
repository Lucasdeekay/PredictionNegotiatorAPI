from django.contrib import admin

from MyApp.models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'upload_date')


admin.site.register(Product, ProductAdmin)
