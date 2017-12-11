# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from shop.models import Product
from placeorder.models import Order, OrderLine
from placeorder.forms import OrderCreateForm
from shoppingcart.shoppingcart import ShoppingCart

# Create your views here.

def createOrder(request):
	_shoppingcart = ShoppingCart(request)
	if len(_shoppingcart)>0:
		form = OrderCreateForm()
		return render(request, 'placeorder/createOrder.html', { 'form': form, 'items': _shoppingcart.cart.items, 'total_price': _shoppingcart.get_total_price() })
	else:
		return redirect('shoppingcart_list')

def confirmOrder(request):
	if request.method == 'POST':
	
		form = OrderCreateForm(request.POST)
	
		if form.is_valid():
			#Saves the order
			order = form.save()
			#Update stock and clear shoppingcart
			_shoppingcart = ShoppingCart(request)
			
			for item in _shoppingcart:
				orderline = OrderLine(order = order, product = item['product'], units = item['units'], pricePerUnit = item['price'])
				orderline.save()
			
			_shoppingcart.updateStock()
			_shoppingcart.clear()
			id = order.id
		else:
			id = None
	return render(request, 'placeorder/confirmOrder.html', {'order_id': id })

