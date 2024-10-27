from django import forms
from .models import Car
from .models import Driver
from .models import Trip

# Машина
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'license_plate', 'year', 'fuel_consumption_per_km', 'mileage']
class DeleteCarForm(forms.Form):
    car_id = forms.IntegerField(label='ID автомобиля для удаления')


# Водитель:
class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'total_mileage']

class DeleteDriverForm(forms.Form):
    driver_id = forms.IntegerField(label='ID водителя для удаления')



# Поездка:
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['driver', 'car', 'departure_time', 'arrival_time', 'distance', 'fuel_spent']
        """
        labels = {
            'driver': 'Водитель',
            'car': 'Автомобиль',
            'departure_time': 'Время выезда',
            'arrival_time': 'Время прибытия',
            'distance': 'Расстояние',
            'fuel_spent': 'Затраченное топливо',
        }
        """
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

class DeleteTripForm(forms.Form):
    trip_id = forms.IntegerField(label='ID водителя для удаления')