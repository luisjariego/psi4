# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from shoppingcart import ShoppingCart
from shop.models import Product
from forms import CartAddProductForm

def shoppingcart_list(request):
	_shoppingcart = ShoppingCart(request)
	for i in _shoppingcart: #TODO NECESARIO ITERAR PARA QUE MUESTRE EL TOTAL PRICE?
		print i
	return render(request, 'shoppingcart/list.html',
					{'shoppingcart': _shoppingcart})

def shoppingcart_add(request, product_id):
	if request.method == 'POST':
		shoppingcart = ShoppingCart(request)
	
		try:
			product = Product.objects.get(id = product_id);
		except Product.DoesNotExist:
			product = None
	
		form = CartAddProductForm(request.POST)
		units = 0
		update_units = False
	
		if form.is_valid():
			if product is not None:
				units = form.cleaned_data['units']
				update_units = form.cleaned_data['update']	 
	
		shoppingcart.addProduct(product=product, units=units, update_units=update_units)
	return redirect('shoppingcart_list')

def shoppingcart_remove(request, product_id):
	shoppingcart = ShoppingCart(request)

	try:
		product = Product.objects.get(id = product_id);
	except Product.DoesNotExist:
		product = None 

	shoppingcart.removeProduct(product=product)
	return redirect('shoppingcart_list')

