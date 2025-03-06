
import django
from asgiref.sync import sync_to_async
import os
import sys
from django import setup
from datetime import datetime
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


@sync_to_async
def check_user(tg_id):
    user = User.objects.filter(tg_id=tg_id).first()
    if user:
        return True
    return False

@sync_to_async
def create_user(tg_id, fio, phone_number):
    user = User.objects.create(tg_id=tg_id,fio=fio,phone_number=phone_number)
    return user

@sync_to_async
def create_order(order_input):
    new_order = Order()
    tg_id = order_input['tg_id']
    user = User.objects.filter(tg_id=tg_id).first()
    print(tg_id,user)
    dt =  datetime(order_input['year'], order_input['month'], order_input['day'], order_input['hours'], order_input['minutes'])
    new_order.user = user
    new_order.adress = order_input['address']
    new_order.date = dt
    if 'text' in order_input:
        new_order.title = order_input['text']
    new_order.level = Cake_levels.objects.filter(id=order_input['level']).first() 
    new_order.shape = Cake_Shape.objects.filter(id=order_input['form']).first()
    if 'berries' in order_input:
        new_order.berries = Cake_Berries.objects.filter(id=order_input['berries']).first()
    if 'decor' in order_input:
        new_order.decor = Cake_Decor.objects.filter(id=order_input['decor']).first()
    if 'topping' in order_input:
        new_order.topping = Cake_Topping.objects.filter(id=order_input['topping']).first()
    if 'comments' in order_input:
        new_order.comment = order_input['comment']
    new_order.save()
    return new_order

@sync_to_async
def get_my_orders(tg_id):
    user = User.objects.filter(tg_id=tg_id).first()
    orders = Order.objects.filter(user=user)
    orders = [order for order in orders]
    return orders


