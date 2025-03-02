from django.db import models
from datetime import datetime, timedelta

class Cake_levels(models.Model):
    name = models.CharField(
        "Кол-во уровней торта",
        max_length=20,
        null=False,
        blank=False
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Уровень торта"
        verbose_name_plural = "Уровни тортов"

    def __str__(self):
        return f'{self.name} - {self.price}р'


class Cake_Shape(models.Model):
    name = models.CharField(
        "Форма торта",
        max_length=20,
        null=False,
        blank=False
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Форма торта"
        verbose_name_plural = "Формы тортов"

    def __str__(self):
        return f'{self.name} - {self.price}р'


class Cake_Topping(models.Model):
    name = models.CharField(
        "Топпинг торта",
        max_length=30,
        null=False,
        blank=False
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Топпинг"
        verbose_name_plural = "Топпинги"

    def __str__(self):
        return f'{self.name} - {self.price}р'


class Cake_Berries(models.Model):
    name = models.CharField(
        "Ягоды для торта",
        max_length=50,
        blank=False,
        null=False
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Ягода для торта"
        verbose_name_plural = "Ягоды для тортов"

    def __str__(self):
        return f'{self.name} - {self.price}р'


class Cake_Decor(models.Model):
    name = models.CharField(
        "Декор для торта",
        max_length=50,
        blank=False,
        null=False
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Декор"
        verbose_name_plural = "Декоры"

    def __str__(self):
        return f'{self.name} - {self.price}р'


class User(models.Model):
    tg_id = models.CharField("tg id пользователя",
                             max_length=50, db_index=True)
    fio = models.CharField(
        "ФИО",
        max_length=20,
        null=True
    )
    phone_number = models.CharField(
        "Номер владельца",
        max_length=20,
        null=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.name} {self.phone_number}'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    adress = models.CharField("Адресс доставки", max_length=100)
    date = models.DateTimeField("Дата доставки", null=False)
    comment = models.TextField(
        "Комментарий к заказу", max_length=1000, null=True)
    title = models.CharField("Надпись на торте", max_length=50, null=True)
    level = models.ForeignKey(
        Cake_levels, on_delete=models.CASCADE, null=True, blank=True)
    shape = models.ForeignKey(
        Cake_Shape, on_delete=models.CASCADE, null=True, blank=True)
    berries = models.ForeignKey(
        Cake_Berries, on_delete=models.CASCADE, null=True)
    decor = models.ForeignKey(Cake_Decor, on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

        def save(self, *args, **kwargs):
            total = 0

            if self.level:
                total += self.level.price

            if self.shape:
                total += self.shape.price

            if self.berries:
                total += self.berries.price

            if self.decor:
                total += self.decor.price

            if self.topping:
                total += self.topping.price

            # Доплата за срочную доставку 
            if self.date and self.date <= datetime.now() + timedelta(hours=24):
                total *= 1.2  

            
            if self.title:
                total += 500  

            self.total_price = total
            super().save(*args, **kwargs)

        def __str__(self):
            return f'Заказ {self.id} для {self.user} на {self.date.strftime("%d.%m.%Y %H:%M")}'
