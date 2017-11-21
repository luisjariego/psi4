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

    def add_product(self,cat, name, description, price, stock):
        from django.core.files import File
        # image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)

        p = Product.objects.get_or_create(category=cat,
                                          prodName=name,
                                          description=description,
                                          price=price,
                                          stock=stock,
                                          image=self.get_image_file())[0]

        return p

    def add_cat(self, name):
        c = Category.objects.get_or_create(catName=name)[0]
        return c

    def populate_data_base(self):
        categories = []
        for counter in range(0,3):
            categories.append(self.add_cat("cat_%d"%counter))
        # cat_1
        for counterCat in range(0,3):
          for counterProd in range(0,5):
            fileName    = "fileName_%d_%d"%(counterCat,counterProd)
            fileNameExt = "test.png"
            self.add_product(cat=categories[counterCat],
                        name=fileName,
                        description="description_%d_%d"%(counterCat,counterProd),
                        price=counterProd + 100*counterCat,
                        stock=counterProd + 10*counterCat
                        )

    def test_produnct_list(self):
        response = self._client.get(reverse('product_list'), follow=True)
        for counter in range(0,3):
            self.assertIn(b'%s'%("cat_%d"%counter), response.content)
        for counterCat in range(0, 3):
            for counterProd in range(0, 5):
                self.assertIn(b"fileName_%d_%d"%(counterCat,counterProd), response.content)

    def test_produnct_list_cat_0(self):
        response = self._client.get(reverse('product_list_by_category',
                                            kwargs={'catSlug':'cat_0'}), follow=True)
        for counter in range(0, 3):
            self.assertIn(b'%s' % ("cat_%d" % counter), response.content)
        for counterCat in range(0, 1):
            for counterProd in range(0, 5):
                self.assertIn(b"fileName_%d_%d" % (counterCat, counterProd), response.content)
        for counterCat in range(1, 3):
            for counterProd in range(0, 5):
                self.assertNotIn(b"fileName_%d_%d" % (counterCat, counterProd), response.content)

    def test_product_detail_fileName_0_0(self):
        prodName='fileName_0_0'
        p = Product.objects.get(prodName = prodName)
        response = self._client.get(reverse('product_detail',
                                            kwargs={'id':p.id,
                                                    'prodSlug':p.prodSlug}), follow=True)
        self.assertIn   (b'cat_0', response.content)
        self.assertNotIn(b'cat_1', response.content)

        self.assertIn(b'description_0_0', response.content)
        self.assertNotIn(b'description_0_1', response.content)
