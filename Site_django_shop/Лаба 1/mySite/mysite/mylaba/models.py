from django.db import models
from django.urls import reverse, reverse_lazy

# Create your models here.
class Clients(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    total_purchase = models.PositiveIntegerField()
    account = models.PositiveIntegerField()
    loan_limit = models.PositiveIntegerField()
    loan_balance = models.PositiveIntegerField()

    def __str__(self):
        return self.surname

    def get_absolute_url(self):
        return reverse('client', kwargs={'clientid': self.pk})

    class Meta():
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']

class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/products/")
    price = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'productid': self.pk})

    class Meta():
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

class Category(models.Model):
    name = models.TextField(max_length=100, db_index=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('catalog-category', kwargs={'cat_slug': self.slug})

    class Meta():
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Cart(models.Model):
    product = models.ForeignKey('Products', on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def line_total(self):
        return self.quantity * self.price


# .filter .exclude .get .all .save .create .order_by .delete