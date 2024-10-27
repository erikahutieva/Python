from django.db import models

# Create your models here.
class Points(models.Model):
    x = models.FloatField()
    y = models.FloatField()
