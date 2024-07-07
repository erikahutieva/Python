from django.db import models
from datetime import date


class Goods(models.Model):
    date = models.DateField(default=date.today(), verbose_name = "Дата")
    name = models.CharField(max_length=200, verbose_name = "Название")
    price = models.FloatField(verbose_name = "Цена")
    amount = models.PositiveSmallIntegerField(verbose_name = "Количество")

    def __str__(self):
        return self.name

    def total_price(self):
        return self.price * self.amount