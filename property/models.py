from django.db import models



class Cake_levels(models.Model):
    levels = models.CharField(
        max_length=20,
        null=False,
        blank=False
        )
    
    def __str__(self):
        return 

class Cake_Shape(models.Model):
    name = models.CharField(
        max_length=20,
        null=False,
        blank=False
        )


class Cake_Topping(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False
        )


class Cake_Berries(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
        )


class Cake_Decor(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
        )


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    adress = models.CharField(max_length=100)
    date = models.DateTimeField()
    comment = models.TextField(max_length=1000, null=True)
    title = models.CharField(max_length=50)
    
    level = models.ForeignKey(Cake_levels, on_delete=models.CASCADE)
    shape = models.ForeignKey(Cake_Shape, on_delete=models.CASCADE)
    berries = models.ForeignKey(Cake_Berries, on_delete=models.CASCADE)
    decor = models.ForeignKey(Cake_Decor, on_delete=models.CASCADE)
    
    
class User (models.Model):
    tg_id = models.CharField(max_length=50)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)