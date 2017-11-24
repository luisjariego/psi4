# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from shoppingcart import ShoppingCart
def shoppingcart_list(request):
	_shoppingcart = ShoppingCart(request)
	return render(request, 'shoppingcart/list.html',
					{'shoppingcart': _shoppingcart})

	