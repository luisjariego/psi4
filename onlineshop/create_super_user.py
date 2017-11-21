#!/usr/bin/env python	
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineshop.settings')

import django
django.setup()

from django.contrib.auth.models import User

u = User(username='alumnodb')
u.set_password('alumnodb')
u.is_superuser = True
u.is_staff = True
u.save()
