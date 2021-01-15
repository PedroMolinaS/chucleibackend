import os
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apis_products.settings')

import django

django.setup()

from django.contrib.auth.models import Group

GROUPS = ['admin', 'anonymus', 'clientefinal']
# MODELS =['user']

for grup in GROUPS:
    new_group, created = Group.objects.get_or_create(name=grup)
