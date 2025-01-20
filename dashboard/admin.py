from django.contrib import admin
from .models import Product, Order
from django.contrib.auth.models import Group
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
     list_display = ('name', 'category', 'quantity', 'expiry_date')
     list_filter = ['category']
admin.site.site_header = "PharmarcyInventory Dashboard"
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
