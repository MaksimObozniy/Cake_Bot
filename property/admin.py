from django.contrib import admin
from .models import Cake_levels, Cake_Shape, Cake_Topping, Cake_Berries, Cake_Decor, User, Order


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'tg_id')
    search_fields = ('phone_number', 'tg_id')
    ordering = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'adress', 'date', 'total_price')
    search_fields = ('user__phone_number', 'adress', 'title')
    list_filter = ('date',)
    ordering = ('-date',)

    def save_model(self, request, obj, form, change):
        obj.save()


@admin.register(Cake_Decor)
class CakeDecorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Cake_levels)
class CakeLevelsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Cake_Shape)
class CakeShapeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Cake_Topping)
class CakeToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Cake_Berries)
class CakeBerriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    ordering = ('name',)
