# Uncomment if you want to run tests in transaction mode with a final rollback
#from django.test import TestCase
#uncomment this if you want to keep data after running tests
from unittest import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from shop.models import Product, Category
from shoppingcart import ShoppingCart
from PIL import Image
from StringIO import StringIO
from django.core.files.base import File

from decimal import Decimal

from views import shoppingcart_list
from forms import CartAddProductForm
#python ./manage.py test shoppingcart.tests.shoppingCartTest --keepdb

DEBUG = False


class shoppingCartTest(TestCase):
    def setUp(self):
        self._client   = Client()
        # self.clean_database()
        # self.populate_data_base()

    # def clean_database(self):
    #     Product.objects.all().delete()
    #     Category.objects.all().delete()

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = StringIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def add_cat(self, name):
        c = Category.objects.get_or_create(catName=name)[0]
        return c

    def add_product(self,cat, name, description, price, stock):
        from django.core.files import File
        products = Product.objects.filter(prodName=name)
        if products.exists():
            p = products[0]
            p.delete()
        p = Product.objects.get_or_create(category=cat,
                                          prodName=name,
                                          description=description,
                                          price=price,
                                          stock=stock,
                                          image=self.get_image_file())[0]

        return p

    def test_shoppingCartAdd(self):
        #CREATE SESSION
        price = 1.1
        stock = 10
        units1 = 1
        units5 = 5
        cat      = self.add_cat("cat_1")
        prod     = self.add_product(cat, "prod", "descript", price, stock)

        response = self._client.get(reverse('product_list'))
        request = response.wsgi_request

        #create shopping cart
        _shoppingcart =  ShoppingCart(request)
        _shoppingcart.addProduct(prod,units=units1)
        _price    = request.session[_shoppingcart.cartKey][str(prod.id)]['price']
        _units = request.session[_shoppingcart.cartKey][str(prod.id)]['units']
        self.assertAlmostEquals(_price,str(price))
        self.assertEquals(_units, units1)

        #update shopping cart 1
        _shoppingcart.addProduct(prod, units=units5,update_units=False)
        _price    = request.session[_shoppingcart.cartKey][str(prod.id)]['price']
        _units = request.session[_shoppingcart.cartKey][str(prod.id)]['units']
        self.assertEquals(_units, units1 + units5)

        #update shopping cart 2
        _shoppingcart.addProduct(prod, units=units5,update_units=True)
        _units = request.session[_shoppingcart.cartKey][str(prod.id)]['units']
        self.assertEquals(_units, units5)

    def test_shoppingCartRemoveProduct(self):
        #CREATE SESSION
        price = 1.1
        stock = 10
        cat      = self.add_cat("cat_1")
        prod1     = self.add_product(cat, "prod1", "descript1", price, stock)
        prod2     = self.add_product(cat, "prod2", "descript2", price, stock)

        response = self._client.get(reverse('product_list'))
        request = response.wsgi_request

        #create shopping cart
        _shoppingcart =  ShoppingCart(request)
        _shoppingcart.addProduct(prod1)
        _shoppingcart.addProduct(prod2)
        key1 = str(prod1.id)
        key2 = str(prod2.id)
        #remove product
        _shoppingcart.removeProduct(prod1)
        _sessionCartDict = request.session[_shoppingcart.cartKey]
        self.assertFalse(key1 in _sessionCartDict)
        self.assertTrue(key2 in _sessionCartDict)

    def test_shoppingCartLen(self):
        #CREATE SESSION
        price = 1.1
        stock = 10
        cat      = self.add_cat("cat_1")
        prod1     = self.add_product(cat, "prod1", "descript1", price, stock)
        prod2     = self.add_product(cat, "prod2", "descript2", price, stock)

        response = self._client.get(reverse('product_list'))
        request = response.wsgi_request

        #create shopping cart
        _shoppingcart =  ShoppingCart(request)
        _shoppingcart.addProduct(prod1,units=3)
        _shoppingcart.addProduct(prod2,units=5)

        #get number of items in sopping cart
        _len = len(_shoppingcart)
        self.assertEqual(_len,8)
        self.assertNotEqual(_len,2)


    def test_shoppingCartTotalPrice(self):
        # CREATE SESSION
        price1 = Decimal(1.1)
        price2 = Decimal(2.2)
        stock = 10
        units1 = 3
        units2 = 5
        cat = self.add_cat("cat_1")
        prod1 = self.add_product(cat, "prod1", "descript1", price1, stock)
        prod2 = self.add_product(cat, "prod2", "descript2", price2, stock)

        response = self._client.get(reverse('product_list'))
        request = response.wsgi_request

        # create shopping cart
        _shoppingcart = ShoppingCart(request)
        _shoppingcart.addProduct(prod1, units=units1)
        _shoppingcart.addProduct(prod2, units=units2)
        totalPrice = _shoppingcart.get_total_price()
        self.assertEqual(totalPrice, price1*units1 +price2*units2)

    def test_shoppingCartList(self):
        # CREATE SESSION
        prodName1 = "prod1"
        prodName2 = "prod2"
        price1 = Decimal(1.1)
        price2 = Decimal(2.2)
        stock = 10
        units1 = 3
        units2 = 5
        cat = self.add_cat("cat_1")
        prod1 = self.add_product(cat, prodName1, "descript1", price1, stock)
        prod2 = self.add_product(cat, prodName2, "descript2", price2, stock)

        response1 = self._client.get(reverse('product_list'))
        request = response1.wsgi_request

        # create shopping cart
        _shoppingcart = ShoppingCart(request)
        _shoppingcart.addProduct(prod1, units=units1)
        _shoppingcart.addProduct(prod2, units=units2)

        #list shopping cart
        response2 = shoppingcart_list(request)
        self.assertIn(prodName1, response2.content)
        self.assertIn(prodName2, response2.content)
        self.assertNotIn("prod3", response2.content)

    def test_shoppingCartListWeb(self):
        # CREATE SESSION
        prodName1 = "prod1"
        prodName2 = "prod2"
        price1 = Decimal(1.1)
        price2 = Decimal(2.2)
        stock = 10
        units1 = 3
        units2 = 5
        cat = self.add_cat("cat_1")
        prod1 = self.add_product(cat, prodName1, "descript1", price1, stock)
        prod2 = self.add_product(cat, prodName2, "descript2", price2, stock)

        response1 = self._client.get(reverse('product_list'))
        request = response1.wsgi_request

        # create shopping cart
        _shoppingcart = ShoppingCart(request)
        _shoppingcart.addProduct(prod1, units=units1)
        _shoppingcart.addProduct(prod2, units=units2)

        #list shopping cart
        response2 = shoppingcart_list(request)
        f = open("/tmp/delete.html",'wb')
        f.write(response2.content)
        f.close()
        from selenium import webdriver
        import time
        driver = webdriver.Chrome()
        driver.get("file:///tmp/delete.html")
        self.assertTrue(True)
        time.sleep(20)

    def test_blank_form(self):
        form = CartAddProductForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'units': [u'This field is required.'],
        })

    def test_valid_form(self):
        form = CartAddProductForm({
            'units': 7,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['units'], 7)
        self.assertEqual(form.cleaned_data['update'], False)

#    def test_shoppingCartListWeb(self):
#         def request(driver):
#             s = requests.Session()
#             cookies = driver.get_cookies()
#             for cookie in cookies:
#                 s.cookies.set(cookie['name'], cookie['value'])
#             return s
#
#         from selenium import webdriver
#         from selenium.webdriver.support.ui import Select
#         import unittest, time, os
#
#         # CREATE SESSION
#         prodName1 = "prod1"
#         prodName2 = "prod2"
#         price1 = Decimal(1.1)
#         price2 = Decimal(2.2)
#         stock = 10
#         units1 = 3
#         units2 = 5
#         cat = self.add_cat("cat_1")
#         prod1 = self.add_product(cat, prodName1, "descript1", price1, stock)
#         prod2 = self.add_product(cat, prodName2, "descript2", price2, stock)
#
#         #open web page
#         base_url     = "http://127.0.0.1:8000"
#         driver = webdriver.Chrome()
#         driver.get(os.path.join(base_url,'.'))
#         request = request(driver)
#
#         # response1 = self._client.get(reverse('product_list'))
#         # request = response1.wsgi_request
#
#         # create shopping cart
#         _shoppingcart = ShoppingCart(request)
#         _shoppingcart.addProduct(prod1, units=units1)
#         _shoppingcart.addProduct(prod2, units=units2)
#         session = request.session['shoppingCart']
#         for key, value in session.iteritems():
#             print "session", key, value
#         c = request.COOKIES
#         for key, value in c.iteritems():
#             print "c", key, value
#         import pickle
#         pickle.dump(driver.get_cookies(), open("one.pkl", "wb"))
#
#         driver.add_cookie({'name': 'shoppingCart', 'value': session})
#         pickle.dump(driver.get_cookies(), open("two.pkl", "wb"))
#         driver.get(os.path.join(base_url,'shoppingcart/list/'))
# #        driver.get(os.path.join(base_url,reverse('shoppingcart_list')))
#         time.sleep(20)
