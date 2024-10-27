from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=100, verbose_name="Марка")
    license_plate = models.CharField(max_length=20, verbose_name="Гос номер")
    year = models.IntegerField(verbose_name="Год выпуска")
    fuel_consumption_per_km = models.FloatField(verbose_name="Расход топлива на 1км")
    mileage = models.FloatField(default=0, verbose_name="Пробег")

    def __str__(self):
        return self.brand

class Driver(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    total_mileage = models.FloatField(default=0, verbose_name="Пробег на всех авто.")

    def __str__(self):
        return self.name

class Trip(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Водитель")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    
    departure_time = models.DateTimeField(verbose_name="Время выезда")
    arrival_time = models.DateTimeField(verbose_name="Время прибытия")
    distance = models.FloatField(verbose_name="Расстояние")
    fuel_spent = models.FloatField(verbose_name="Затраченное топливо")

    
    def save(self, *args, **kwargs):
        # При сохранении путевого листа обновляем суммарный пробег водителя и суммарный пробег автомобиля
        self.driver.total_mileage += self.distance
        self.driver.save()
        self.car.mileage += self.distance
        self.car.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.driver.name} - {self.car.brand}"