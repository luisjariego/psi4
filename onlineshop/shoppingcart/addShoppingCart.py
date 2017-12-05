from shoppingcart import ShoppingCart

def addShoppingCart(request):
	return {'shoppingcart' : ShoppingCart(request)}