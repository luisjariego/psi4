
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from shop.models import Product
import onlineshop.settings as settings

# Create your models here.
class Order(models.Model):
	firstName = models.CharField(max_length=128)
	familyName = models.CharField(max_length=128)
	email = models.EmailField(max_length=128) #unique=True?
	address = models.CharField(max_length=128)
	zip = models.CharField(max_length=128)
	city = models.CharField(max_length=128)
	created = models.DateTimeField(default = timezone.now)
	updated = models.DateTimeField(default = timezone.now)
	paid = models.BooleanField(default=False)
	
	def save(self, *args, **kwargs):
		super(Order, self).save(*args, **kwargs)

	def getTotalCost():
		return sum(item.getProductCost() for item in OrderLine.objects.filter(order = self))

	def __str__(self): #TODO cambiar
		return self.firstName + " " + self.familyName
	
	#def getTotalCost():
	#	for item in Orderline.OrderLine_set.all():
	
	#def getTotalCost():
	#	orders = OrderLine.objects.filter(order = self)
	#	total = 0
	#	for item in orders:
	#		total += item.getProductCost()
			

class OrderLine(models.Model):
	order = models.ForeignKey(Order, related_name='orderLines')
	product = models.ForeignKey(Product, related_name='productLines')
	units = models.IntegerField(default=0)
	pricePerUnit = models.DecimalField(decimal_places = 2, max_digits=12 , default=0)
	
	def save(self, *args, **kwargs):
		super(OrderLine, self).save(*args, **kwargs)
	
	def getProductCost():
		return units * pricePerUnit
	
	def __str__(self): #TODO cambiar
		return self.product.prodName

