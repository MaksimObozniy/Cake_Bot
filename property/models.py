from django.db import models



class Cake_levels(models.Model):
    levels = models.CharField(
        "Кол-во уровней торта",
        max_length=20,
        null=False,
        blank=False
        )
    
    def __str__(self):
        return 

class Cake_Shape(models.Model):
    name = models.CharField(
        "Форма торта",
        max_length=20,
        null=False,
        blank=False
        )


class Cake_Topping(models.Model):
    name = models.CharField(
        "Топпинг торта"
        max_length=30,
        null=False,
        blank=False
        )


class Cake_Berries(models.Model):
    name = models.CharField(
        "Ягоды для торта",
        max_length=50,
        blank=False,
        null=False
        )


class Cake_Decor(models.Model):
    name = models.CharField(
        "Декор для торта",
        max_length=50,
        blank=False,
        null=False
        )


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    adress = models.CharField("Адресс доставки", max_length=100)
    date = models.DateTimeField("Дата доставки", null=False)
    comment = models.TextField("Комментарий к заказу", max_length=1000, null=True)
    title = models.CharField("Надпись на торте", max_length=50, null=True)
    
    level = models.ForeignKey(Cake_levels, on_delete=models.CASCADE)
    shape = models.ForeignKey(Cake_Shape, on_delete=models.CASCADE)
    berries = models.ForeignKey(Cake_Berries, on_delete=models.CASCADE)
    decor = models.ForeignKey(Cake_Decor, on_delete=models.CASCADE)
    
    
class User (models.Model):
    first_name = models.CharField("Имя клиента", max_length=20)
    phone_number = models.CharField(
        "Номер владельца",
        max_length=20,
        db_index=True
        )
    
    tg_id = models.CharField("tg id пользователя", max_length=50)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="История заказов")