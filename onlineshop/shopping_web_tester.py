    # -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest, time, os
from django.template.defaultfilters import slugify
try:
   from loremipsum import get_paragraphs
except:
   def get_paragraphs():
       return "Y, viéndole don Quijote de aquella manera, con muestras de " \
              "tanta tristeza, le dijo: Sábete, Sancho, que no es un hombre " \
              "más que otro si no hace más que otro. Todas estas borrascas " \
              "que nos suceden son señales de que presto ha de serenar el " \
              "tiempo y han de sucedernos bien las cosas; porque no es posible " \
              "que el mal ni el bien sean durables, y de aquí se sigue que, " \
              "habiendo durado mucho el mal, el bien está ya cerca. Así que, " \
              "no debes congojarte por las desgracias que a mí me suceden, " \
              "pues a ti no te cabe parte dellas."
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onLineShop.settings')
#import django
#django.setup()

#from shop.models import Product

class onLineShopTester(unittest.TestCase):
    POPULATE      = True # set to True if you  want to populate the database
    ADDPRODUCT    = True # set to True if you  want to add
                          # products to the shoppingcart
    REMOVEPRODUCT = True # set to True if you  want to remove
                          # products from the shoppingcart
    CHECKOUT      = True # press checkout botton
    PLACEORDER    = True # place order. The END ;-)
    username    = "alumnodb"
    passwd      = "alumnodb"
    #base_url     = "https://quiet-scrubland-14247.herokuapp.com/"
    base_url = "http://127.0.0.1:8000"
    admin_url    = base_url + "/admin/"
    shoppingcart_url = base_url + "/cart/"
    create_order_url      = base_url + "/orders/create_order/"
    confirm_order_url = base_url + "/orders/confirm_order/"
    addCategoryPath = "shop/category/add/"
    addProductPath  = "shop/product/add/"
    catList = ["Microwave ovens","Washing machines","Refrigerators"]
    washing_machines = ["Bosch WAQ 28468 LCD Display A+++",
                  "Beko WTE6511BW 39L A+++",
                  "Balay 3TS976BA A+++",
                  "Siemens WM14Q468ES Digital display A+++",
                  "Kenmore 28132 Top Load Washer in White",
                  "Kenmore Elite 51993 Wide Pedestal Washer"]
    microwaves = ["Microwave TAURUS 970930",
                  "Taurus 970921000 LUXUS GRILL",
                  "Samsung GE731 K microwave",
                  "Whirlpool AMW 160 Grill",
                  "Samsung MS11K3000AS Countertop Microwave",
                  "Hamilton Beach 900W Microwave"]
    refrigerators = ["Samsung Refrigerator in Stainless Steel",
                     "Frigidaire Refrigerator in Black Stainless Steel",
                     "American fridge - Samsung RS7528THCSL A++ Display Inox",
                     "Balay fridge 3FC1601B 186cm A++ LEDs",
                     "Danby 120 Can Beverage Center",
                     "Della Mini Compact Refrigerator Freezer White"]
    productDict = {"Microwave ovens":  microwaves, 
        "Washing machines": washing_machines, 
        "Refrigerators": refrigerators
        }
    driverPath=os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'ficheros_psi3/chromedriver')
    imagesPath = os.path.join( os.path.dirname(os.path.abspath(__file__)), "images/")
    purchaseCost = "136.40"

    def setUp(self):
#        self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(self.driverPath)
############################################
##DO NOT CHANGE ANYTHING BELLOW THIS POINT
###########################################
    def find_element_by_id(self,_id,value,waitFor=1):
        self.driver.find_element_by_id(_id).clear()
        self.driver.find_element_by_id(_id).send_keys(value)
        time.sleep(waitFor)

    def find_element_by_xpath(self,_xpath,waitFor=1):
        self.driver.find_element_by_xpath(_xpath).click()
        time.sleep(waitFor)

    def find_element_by_name(self,_name,waitFor=1):
        self.driver.find_element_by_name(_name).click()
        time.sleep(waitFor)

    def find_element_by_link_text(self, _link, waitFor=1):
        self.driver.find_element_by_link_text(_link).click()
        time.sleep(waitFor)

    def get_url(self, url, waitFor=1):
        self.driver.get(url)

        time.sleep(waitFor)

    def login(self,userName, passwd):
        self.get_url(self.admin_url)
        self.find_element_by_id("id_username",userName)
        self.find_element_by_id("id_password",passwd)
        self.find_element_by_xpath('//*[@id="login-form"]/div[3]/input')

    def addCat(self,catName, waitFor=1):
        self.get_url(self.admin_url + self.addCategoryPath)
        self.find_element_by_id("id_catName",catName, waitFor)
        self.find_element_by_name("_save", waitFor)

    def addProduct(self, cat, prodName, ext="jpg", price="1.1", stock="10", waitFor=1):
        self.get_url(self.admin_url + self.addProductPath)

        select = Select(self.driver.find_element_by_id('id_category'))
        select.select_by_visible_text(cat)

        self.find_element_by_id("id_prodName",prodName, waitFor)
        imagePath =  os.path.join(self.imagesPath,cat.lower(),prodName+"."+ext)
        #self.driver.find_element_by_id("id_image").send_keys(imagePath)######
        self.find_element_by_id("id_image",imagePath)
        self.find_element_by_id("id_description",get_paragraphs(1)[0], waitFor)
        self.find_element_by_id("id_price",price, waitFor)
        self.find_element_by_id("id_stock",stock, waitFor)
        self.find_element_by_name("_save", waitFor)

    def selectProduct(self, id, prodSlug, units=1, waitFor=1):
        self.get_url(os.path.join(self.base_url,str(id),prodSlug))
        try:
            self.selectProductInteger(units, waitFor)
        except:
            self.selectProductList(units, waitFor)

    def selectProductInteger(self, units=1, waitFor=1):
        """ units as an IntegerField"""
        self.find_element_by_id("id_units", units, waitFor)
        self.find_element_by_xpath('//*[@id="content"]/div/form/input[4]')

    def selectProductList(self, units=1, waitFor=1):
        """units as a list"""
        select = Select(self.driver.find_element_by_id('id_units'))
        select.select_by_visible_text(str(units))
        #self.find_element_by_xpath('//*[@id="content"]/div/form/input[3]')
        self.find_element_by_xpath('//form/input[3]')
        self.assertEqual(self.driver.current_url, self.shoppingcart_url)

    def removeProduct(self, id, prodSlug, waitFor=1):
        self.get_url(self.shoppingcart_url)
        time.sleep(waitFor)
        self.find_element_by_link_text("Remove")
        #self.find_element_by_xpath('//tr[2]/td[4]')
#                                   //*[@id="content"]/table/tbody/tr[1]/td[4]

    def fillOrderCreateForm(self, firstName, familyName,
                                  email, address, zip, city, waitFor=1):
        if self.driver.current_url == self.shoppingcart_url:
            self.find_element_by_link_text("Checkout")
        else:
            self.get_url(self.create_order_url)
        self.find_element_by_id("id_firstName", firstName)
        self.find_element_by_id("id_familyName", familyName)
        self.find_element_by_id("id_email", email)
        self.find_element_by_id("id_address", address)
        self.find_element_by_id("id_zip", zip)
        self.find_element_by_id("id_city", city)
        #text = self.purchaseCost
        #self.assertTrue(text in self.driver.page_source)

        time.sleep(waitFor)

    def placeOrder(self, waitFor=1):
        self.find_element_by_xpath(
            "//input[@type='submit' and @value='Place order']")
        time.sleep(waitFor)
        self.assertEqual(self.driver.current_url, self.confirm_order_url)

    def seeHome(self, waitFor=1):
        self.get_url(self.base_url, waitFor=1)

    def quit(self, waitFor=1):
        time.sleep(waitFor)
        self.driver.quit()

    def test_shop(self):
        #connect to Home
        self.seeHome(2)

        if self.POPULATE:
            #login in
            self.login(self.username, self.passwd)

            #addCategories
            for catName in self.catList:
                self.addCat(catName,1)

            #addProducts
            counter =2
            for catName in self.catList:
                for prodName in self.productDict[catName]:
                    self.addProduct(catName,prodName,
                                    price = str(counter * 1.1),
                                    stock = str(counter), waitFor = 0)
                    counter += 1

            #connect to Home
            self.seeHome(1)

        id1 = 1; id2 = 8; id3 = 15; id4=16
        prodSlug1 = slugify(self.productDict[self.catList[0]][0])
        prodSlug2 = slugify(self.productDict[self.catList[1]][1])
        prodSlug3 = slugify(self.productDict[self.catList[2]][2])
        prodSlug4 = slugify(self.productDict[self.catList[2]][3])
        if self.ADDPRODUCT:  #select several products
            self.selectProduct(id1, prodSlug1, units=2, waitFor=1)
            self.selectProduct(id2, prodSlug2, units=3, waitFor=1)
            self.selectProduct(id3, prodSlug3, units=4, waitFor=1)
            self.selectProduct(id4, prodSlug4, units=4, waitFor=1)

        if self.REMOVEPRODUCT:
            self.removeProduct(id2, prodSlug2, waitFor=1)
            self.removeProduct(id3, prodSlug3, waitFor=1)

        if self.CHECKOUT:
            self.fillOrderCreateForm('Julius', 'Caesar',
                                     'julius@rome.it',
                                     'Imperial Place, Pallatinus Hill',
                                     '12345', 'Rome')

            if self.PLACEORDER:
                self.placeOrder()
        #close browser
        self.quit(20)

if __name__ == "__main__":
    unittest.main()

"""

"""
