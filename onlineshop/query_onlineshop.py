#!/usr/bin/env python
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineshop.settings')

django.setup()
from django.db import models
from django.core.files import File
from shop.models import Category, Product
import onlineshop.settings as settings

def query():
    #1
	catdeals = "deals"
	c = Category.objects.filter(catName = catdeals)
	if not c.exists():
		add_cat(catdeals)
		print "Category \"" + catdeals + "\" created"
	else:
		print "Category \"" + catdeals + "\" already exists"
	#2
	catbargains = "bargains"
	c = Category.objects.filter(catName = catbargains)
	if not c.exists():
		add_cat(catbargains)
		print "Category \"" + catbargains + "\" created"
	else:
		print "Category \"" + catbargains + "\" already exists"
	#3
	c = Category.objects.get(catName = catdeals)
	prodeal1 = "deal 1"
	p = Product.objects.filter(prodName = prodeal1)
	if not p.exists():
		add_product(c, prodeal1, 'deal.jpg', "", 1, 0, False)
		print "Product named \"" + prodeal1 + "\" created"
	else:
		print "Product named \"" + prodeal1 + "\" already exists"
	
	prodeal2 = "deal 2"
	p = Product.objects.filter(prodName = prodeal2)
	if not p.exists():
		add_product(c, prodeal2, 'deal.jpg', "", 1, 0, False)
		print "Product named \"" + prodeal2 + "\" created"
	else:
		print "Product named \"" + prodeal2 + "\" already exists"
	
	prodeal3 = "deal 3"
	p = Product.objects.filter(prodName = prodeal3)
	if not p.exists():
		add_product(c, prodeal3, 'deal.jpg', "", 1, 0, False)
		print "Product named \"" + prodeal3 + "\" created"
	else:
		print "Product named \"" + prodeal3 + "\" already exists"
	
	#4
	c = Category.objects.get(catName = catbargains)
	probargain1 = "bargain 1"
	p = Product.objects.filter(prodName = probargain1)
	if not p.exists():
		add_product(c, probargain1, 'bargain.jpg', "", 1, 0, False)
		print "Product named \"" + probargain1 + "\" created"
	else:
		print "Product named \"" + probargain1 + "\" already exists"
	
	probargain2 = "bargain 2"
	p = Product.objects.filter(prodName = probargain2)
	if not p.exists():
		add_product(c, probargain2, 'bargain.jpg', "", 1, 0, False)
		print "Product named \"" + probargain2 + "\" created"
	else:
		print "Product named \"" + probargain2 + "\" already exists"
	
	probargain3 = "bargain 3"
	p = Product.objects.filter(prodName = probargain3)
	if not p.exists():
		add_product(c, probargain3, 'bargain.jpg', "", 1, 0, False)
		print "Product named \"" + probargain3 + "\" created"
	else:
		print "Product named \"" + probargain3 + "\" already exists"
	
	#5
	cat = Category.objects.get(catName = catbargains)
	prodlist = Product.objects.filter(category=cat)
	#6
	print "Products related to Category \"" + catbargains + "\":"
	print prodlist
	#7
	proslug = "deal-1"
	prod = Product.objects.get( prodSlug = proslug)
	category = prod.category
	#8
	print "Category associated to the Product with prodSlug=\"" + proslug + "\":" + category.catSlug
	#9
	proslug = "oferta-10"
	prod = Product.objects.filter( prodSlug = proslug)
	if not prod.exists():
		print "Product named \"" + proslug + "\" does not exist."
	else: #Shouldn't go here
		category = prod.cat
		print "Category associated to the Product with prodSlug=\"" + proslug + "\": " + category.catSlug
	

def add_product(cat, prodName, image, description, price, stock, availability):
	imageObject = File(open(os.path.join("images/", image),'r')) #From where we upload it
	p = Product.objects.get_or_create(category=cat, prodName=prodName)[0]
	p.image.save(image, imageObject, save= True)
	p.description=description
	p.price=price
	p.stock=stock
	p.availability=	availability
	p.save()
	return p
def add_cat(catName):
    c = Category.objects.get_or_create(catName=catName)[0]
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting onlineshop query script...")
query()
