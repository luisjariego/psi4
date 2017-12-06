# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from models import Order, OrderLine
from shop.models import Category, Product
from decimal import Decimal

from forms import OrderCreateForm
#python ./manage.py test placeorder.tests.placeOrderTest --keepdb

DEBUG = False


class placeOrderTest(TestCase):

    def setUp(self):
        self._client = Client()

    def test_blank_form(self):
        form = OrderCreateForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['firstName'],
                                    [u'This field is required.']
                        )
        fields = ['firstName', 'familyName', 'email', 'address', 'zip', 'city']

    def fillForm(self):
        form = OrderCreateForm({
            'firstName': 'Julius',
            'familyName': 'Caesar',
            'email': 'Julius@rome.it',
            'address': 'Imperial Palace, Pallatinus Hill',
            'zip': '12345',
            'city': 'rome',
        })
        return form

    def test_valid_form(self):
        form = self.fillForm()
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['firstName'], 'Julius')
        self.assertEqual(form.cleaned_data['familyName'], 'Caesar')
        self.assertEqual(form.cleaned_data['email'], 'Julius@rome.it')
        self.assertEqual(form.cleaned_data['zip'], '12345')
        self.assertEqual(form.cleaned_data['address'], 'Imperial Palace, Pallatinus Hill')

    def createOrder(self):
        form = self.fillForm()
        if form.is_valid():
            order = form.save()
        else:
            order = None
        return order

    def test_Order(self):
        order = self.createOrder()
        self.assertEqual(order.firstName, 'Julius')
        self.assertEqual(order.familyName, 'Caesar')
        self.assertEqual(order.email, 'Julius@rome.it')
        self.assertEqual(order.zip, '12345')
        self.assertEqual(order.address, 'Imperial Palace, Pallatinus Hill')
        self.assertFalse(order.paid)
        import datetime
        now = datetime.datetime.now()
        self.assertEqual(order.created.year,now.year)
        self.assertEqual(order.created.month,now.month)
        self.assertEqual(order.created.day,now.day)
        self.assertEqual(order.created.hour,now.hour)
        self.assertEqual(order.updated.year,now.year)
        self.assertEqual(order.updated.month,now.month)
        self.assertEqual(order.updated.day,now.day)
        self.assertEqual(order.updated.hour,now.hour)

    def test_OrderLine(self):
        from PIL import Image
        from StringIO import StringIO
        from django.core.files.base import File

        def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
            file_obj = StringIO()
            image = Image.new("RGBA", size=size, color=color)
            image.save(file_obj, ext)
            file_obj.seek(0)
            return File(file_obj, name=name)
        def add_cat(name):
            c = Category.objects.get_or_create(catName=name)[0]
            return c

        def add_product(cat, name, description, price, stock):
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
                                              image=get_image_file())[0]

            return p
        units5=5
        cat = add_cat("cat_1")
        product = add_product(cat, "prod_1", "descript_1", 1,2)
        order = self.createOrder()
        orderline = OrderLine(order=order,product=product,
                  pricePerUnit=product.price, units=units5)
        orderline.save()
        self.assertEqual(order.orderLines.first(), orderline)#N->1 relationship
        self.assertEqual(orderline.product,product)
        self.assertEqual(orderline.pricePerUnit, product.price)
        self.assertEqual(orderline.units,units5)
        self.assertEqual(orderline.getProductCost(), orderline.pricePerUnit *
                                                     orderline.units)
        self.assertEqual(order.getTotalCost(),orderline.getProductCost())