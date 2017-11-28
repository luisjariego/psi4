# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from shoppingcart import ShoppingCart
from shop.models import Product
from forms import CartAddProductForm

def shoppingcart_list(request):
	_shoppingcart = ShoppingCart(request)
	print _shoppingcart.cart
	return render(request, 'shoppingcart/list.html',
					{'shoppingcart': _shoppingcart})

def shoppingcart_add(request, product_id):
	if request.method == 'POST':
		shoppingcart = ShoppingCart(request)
	
		try:
			product = Product.objects.get(id = product_id);
		except Product.DoesNotExist:
			product = None
	
		form = CartAddProductForm()
		units = 0
		update_units = False
	
		if form.is_valid():
			if product is not None:
				units = form.cleaned_data['units']
				update_units = form.cleaned_data['update']	 
	
		shoppingcart.addProduct(product=product, units=units, update_quantity=update_units)
	return redirect('shoppingcart_detail')

def shoppingcart_remove(request, product_id):
	
	return redirect('shoppingcart_list')
