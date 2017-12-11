
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

	def getTotalCost(self):
		return sum(item.getProductCost() for item in OrderLine.objects.filter(order = self))

	def __str__(self):
		return self.firstName + " " + self.familyName + "-" + self.email
			

class OrderLine(models.Model):
	order = models.ForeignKey(Order, related_name='orderLines')
	product = models.ForeignKey(Product, related_name='productLines')
	units = models.IntegerField(default=0)
	pricePerUnit = models.DecimalField(decimal_places = 2, max_digits=12 , default=0)
	
	def save(self, *args, **kwargs):
		super(OrderLine, self).save(*args, **kwargs)
	
	def getProductCost(self):
		return self.units * self.pricePerUnit
	
	def __str__(self):
		return self.product.prodName + "(x" + self.units + ")"

