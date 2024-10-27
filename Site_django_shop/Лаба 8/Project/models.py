from django.db import models

class Material(models.Model):
    code = models.CharField(max_length=50, verbose_name = "Код")
    name = models.CharField(max_length=100, verbose_name = "Название")
    sschet = models.CharField(max_length=50, verbose_name = "Ссчёт")
    is_even = models.CharField(max_length=50, default=False)

    def __str__(self):
        return self.name