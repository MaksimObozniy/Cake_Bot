
import django
from asgiref.sync import sync_to_async
import os
import sys
from django import setup

child_directory = os.path.dirname(__file__)
parent_directory = os.path.dirname(child_directory)
sys.path.append(os.path.join(parent_directory, 'Cake_Bot'))
print(sys.path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cake_Bot.settings')


django.setup()

from property.models import Cake_Berries, Cake_Decor, Cake_levels, Cake_Shape, Cake_Topping, Order, User

@sync_to_async
def get_all_levels():
    return list(Cake_levels.objects.all())


@sync_to_async
def get_all_decors():
    return list(Cake_Decor.objects.all())


@sync_to_async
def get_all_berries():
    return list(Cake_Berries.objects.all())


@sync_to_async
def get_all_forms():
    return list(Cake_Shape.objects.all())


@sync_to_async
def get_all_toppings():
    return list(Cake_Topping.objects.all())
