# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from placeorder.models import Order, OrderLine

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
	list_display = ('firstName', 'familyName', 'email', 'address', 'zip', 'paid')

class OrderLineAdmin(admin.ModelAdmin):
	list_display = ('order', 'product', 'units', 'pricePerUnit')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
