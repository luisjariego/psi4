from decimal import Decimal
from shop.models import Product

class ShoppingCart(object):
	cartKey='shoppingCart'
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(self.cartKey)
		if not cart:
			#save empty cart
			cart = self.session[self.cartKey] = {}
		self.cart = cart

	def addProduct(self, product, units=1, update_units=False):
		#dictionary keys should be strings
		product_id = str(product.id)
		if units>0 and units<=product.stock:
			if product_id in self.cart:
				if update_units==True:
					self.cart[product_id]['units'] = units
				else:
					self.cart[product_id]['units'] += units
			else:
				self.cart[product_id] = {'units': units, 'price': str(product.price),
										'prodName': product.prodName, 'total_price': str(units * product.price)} #'image': product.image
		self.saveCart()

	def saveCart(self):
		#update the session cart
		self.session[self.cartKey] = self.cart
		#mark the session as "modified" to make sure it is saved
		self.session.modified = True

	def removeProduct(self, product):
		product_id = str(product.id)
		del self.cart[product_id]
		self.saveCart()

	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item ['total_price'] = item['price'] * item['units']
			yield item

	def __len__(self):
		return sum(item['units'] for item in self)

	def get_total_price(self):
		return sum(item['total_price'] for item in self)

	def get_total_units(self):
		return sum(item['units'] for item in self)

	def clear(self):
		del self.session[self.cartKey]
		self.session.modified = True


