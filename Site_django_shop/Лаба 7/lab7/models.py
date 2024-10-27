from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    inn = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"