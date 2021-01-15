import os
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apis_products.settings')

import django

django.setup()

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['admin', 'anonymus', 'clientefinal']
MODELS = ['Usuario']

for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)
    for model in MODELS:
        if new_group.name == 'admin':
            PERMISSIONS = ['view', 'change', 'add', 'delete']
            for permission in PERMISSIONS:
                name = 'Can {} {}'.format(permission, model)
                try:
                    model_add_perm = Permission.objects.get(name=name)
                except Permission.DoesNotExist:
                    logging.warning("Permiso no existe '{}'.".format(name))
                    continue

                new_group.permissions.add(model_add_perm)

        elif new_group.name == 'anonymus':
            PERMISSIONS = ['view']
            for permission in PERMISSIONS:
                name = 'Can {} {}'.format(permission, model)
                try:
                    model_add_perm = Permission.objects.get(name=name)
                except Permission.DoesNotExist:
                    logging.warning("Permiso no existe '{}'.".format(name))
                    continue

                new_group.permissions.add(model_add_perm)

        elif new_group.name == 'clientefinal':
            PERMISSIONS = ['view', 'add']
            for permission in PERMISSIONS:
                name = 'Can {} {}'.format(permission, model)
                try:
                    model_add_perm = Permission.objects.get(name=name)
                except Permission.DoesNotExist:
                    logging.warning("Permiso no existe '{}'.".format(name))
                    continue

                new_group.permissions.add(model_add_perm)

print("Permisos asignados con exito!!")
