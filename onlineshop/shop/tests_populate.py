# Uncomment if you want to run tests in transaction mode with a final rollback
#from django.test import TestCase
#uncomment this if you want to keep data after running tests
from unittest import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import Client
from shop.models import Product, Category

import os
base_path   = os.getcwd()
static_path = os.path.join(base_path,"static")


#python ./manage.py test shop.tests.viewsTests --keepdb

DEBUG = False
from PIL import Image
from StringIO import StringIO
from django.core.files.base import File

class viewsTests(TestCase):

	microwaves = [
		{"prodName": "Microwave TAURUS 970.930",
		"prodSlug": "TAURUS_970.930",
		"image": "Microwave TAURUS 970.930.jpg",
		"description":"Equip your kitchen with Taurus microwave oven Ready Grill. It will the most beloved tool in your household.",
		"price": 49.90,
		"stock": 1,
		"availability": True } ]
	washing_machines = [
		{"prodName": "Bosch WAQ 28468 LCD Display A+++",
		"prodSlug": "BOSCH_WAQ28468",
		"image": "Bosch WAQ 28468, LCD Display, A+++.jpg",
		"description":"New exterior structure, specially made to be more silent.",
		"price": 389,
		"stock": 7,
		"availability": True} ]
	refrigerators = [ 
		{"prodName": "Samsung Refrigerator in Stainless Steel",
		"image": "Samsung Refrigerator in Stainless Steel.jpg",
		"description":"CoolSelect Pantry provides added temperature control. High-Efficiency LED Lighting helps you quickly spot what you want",
		"price": 998,
		"stock": 5,
		"availability": True} ]
	cats = {"Microwave ovens": {"products": microwaves, "catSlug": "microwaves" },
		"Washing machines": {"products": washing_machines, "catSlug": "washing_machines" },
		"Refrigerators": {"products": refrigerators, "catSlug": "refrigerators" } }
	
	def setUp(self):
		self._client   = Client()
		self.clean_database()
		self.populate_data_base()

	@staticmethod
	def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
		file_obj = StringIO()
		image = Image.new("RGBA", size=size, color=color)
		image.save(file_obj, ext)
		file_obj.seek(0)
		return File(file_obj, name=name)

	def clean_database(self):
		Product.objects.all().delete()
		Category.objects.all().delete()

	def add_product(self, cat, prodName, image, description, price, stock, availability):
		try:
			 p = Product.objects.get(prodName=prodName)
		except Product.DoesNotExist:
			ext='jpg'
			imagePath=os.path.join('images/',cat.catName.lower(),prodName+"."+ext)
			imageObject = File(open(imagePath,'r')) #From where we upload it
			p = Product.objects.create(category=cat, prodName=prodName)
			p.image.save("""%s/%s"""%(cat.catName.lower(), image), imageObject, save= True)
			p.description=description
			p.price=price
			p.stock=stock
			p.availability=	availability
			p.save()
		return p

	def add_cat(self, name):
		c = Category.objects.get_or_create(catName=name)[0]
		c.save()
		return c

	def populate_data_base(self):
		for cat, cat_data in self.cats.items():
			c = self.add_cat(cat)
			for p in cat_data["products"]:
				self.add_product(c, p['prodName'], p['image'], p['description'], p['price'], p['stock'], p['availability'])

	def test_produnct_list(self):
		response = self._client.get(reverse('product_list'), follow=True)
		
		for cat in self.cats:
			self.assertIn(cat, response.content)
			for prod in self.cats[cat]['products']:
				self.assertIn(prod['prodName'], response.content);

	def test_produnct_list_cat_0(self):
		response = self._client.get(reverse('product_list_by_category',
											kwargs={'catSlug':'microwaves'}), follow=True)
		for cat in self.cats:
			if cat == "Microwave ovens":
				self.assertIn(cat, response.content)
				for prod in self.cats[cat]['products']:
					self.assertIn(prod['prodName'], response.content);

	def test_product_detail_fileName_0_0(self):
		prodName='Microwave TAURUS 970.930'
		p = Product.objects.get(prodName = prodName)
		response = self._client.get(reverse('product_detail',
											kwargs={'id':p.id,
													'prodSlug':p.prodSlug}), follow=True)
		self.assertIn   (b'Microwave ovens', response.content)
		#They always appear in the side bar menu
		#self.assertNotIn(b'refrigerators', response.content)
		#self.assertNotIn(b'washing_machines', response.content)

		self.assertIn("Equip your kitchen with Taurus microwave oven Ready Grill. It will the most beloved tool in your household.", response.content)
		self.assertNotIn("New exterior structure, specially made to be more silent.", response.content)

