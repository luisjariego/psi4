# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-31 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20171031_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='catSlug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
