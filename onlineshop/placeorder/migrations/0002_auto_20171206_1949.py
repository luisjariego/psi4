# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placeorder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=128),
        ),
    ]
