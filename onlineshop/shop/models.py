# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime
from django.utils import timezone
import onlineshop.settings as settings

# Create your models here.

class Category(models.Model):
    catName = models.CharField(max_length=128, unique=True)
    catSlug = models.SlugField(blank=True, unique=True)	

    def save(self, *args, **kwargs):
        self.catSlug = slugify(self.catName)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.catName
    def __unicode__(self):
        return self.catName


class Product(models.Model):
    category = models.ForeignKey(Category)
    prodName = models.CharField(max_length=128, unique=True)
    prodSlug = models.SlugField( unique=True, blank=True)
    image = models.ImageField(upload_to = './', null=True)
    description = models.CharField(max_length=1000)
    price = models.DecimalField( decimal_places = 2, max_digits = 8, default = 0) #??
    stock = models.IntegerField( default = 0) #??
    availability = models.BooleanField(default = True)
    created = models.DateTimeField(default = timezone.now) #??
    updated = models.DateTimeField(default = timezone.now) #??
	
    def save(self, *args, **kwargs):
        self.prodSlug = slugify(self.prodName)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.prodName
    def __unicode__(self):
        return self.prodName

