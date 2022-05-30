from django.contrib import admin
from .models import Product, Supplier, Package


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'package')
    list_filter = ('product_type', 'supplier')


admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)
admin.site.register(Package)
