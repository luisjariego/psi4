# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from shop.models import Category, Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
	list_display = ('prodName','category','price', 'stock', 'availability')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
