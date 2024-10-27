from django.contrib import admin
from . import models

admin.site.register(models.Car)
admin.site.register(models.Driver)
admin.site.register(models.Trip)
