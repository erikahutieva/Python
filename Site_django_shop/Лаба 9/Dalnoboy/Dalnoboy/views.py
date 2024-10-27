from django.shortcuts import render, redirect

# Таблицы в БД:
from .models import Car  # Импортируем модель Car
from .models import Driver  # Импортируем модель Driver
from .models import Trip  # Импортируем модель Trip

# Формы:
from . import forms

# переход по URL адресам:
def showIndexPage(request):
    return render(request, 'Dalnoboy/base.html')

def showCarsPage(request):
    if request.method == 'POST':  # Проверяем, была ли отправлена форма методом POST
        ADD_CAR_form = forms.CarForm(request.POST)
        DEL_CAR_form = forms.DeleteCarForm(request.POST)
        if ADD_CAR_form.is_valid():
            ADD_CAR_form.save()
            return redirect('cars')  # Перенаправление на страницу со списком автомобилей
        if DEL_CAR_form.is_valid():
            car_id = DEL_CAR_form.cleaned_data['car_id']
            car = Car.objects.get(pk=car_id)
            car.delete()
            return redirect('cars')  # Обновить страницу типа. Ведь мы в БД запись добавили => надо перерисовать таблицу на html.
    else:
        ADD_CAR_form = forms.CarForm()  # Если запрос не методом POST, создаем пустую форму
        DEL_CAR_form = forms.DeleteCarForm()

    cars = Car.objects.all()  # Получаем все объекты модели Car из базы данных
    context = {'cars': cars,
               'form1': ADD_CAR_form,
               'form2' : DEL_CAR_form}
    return render(request, 'Dalnoboy/cars.html', context)  # Передаем данные о машинах в шаблон


def showDriversPage(request):
    if request.method == 'POST':
        ADD_DRIVER_form = forms.DriverForm(request.POST)
        DEL_DRIVER_form = forms.DeleteDriverForm(request.POST)
        if ADD_DRIVER_form.is_valid():
            ADD_DRIVER_form.save()
            return redirect('drivers')
        if DEL_DRIVER_form.is_valid():
            driver_id = DEL_DRIVER_form.cleaned_data['driver_id']
            driver = Driver.objects.get(pk=driver_id)
            driver.delete()
            return redirect('drivers')
    else:
        ADD_DRIVER_form = forms.DriverForm()
        DEL_DRIVER_form = forms.DeleteDriverForm()

    drivers = Driver.objects.all()
    context = {'drivers': drivers,
               'form1': ADD_DRIVER_form,
               'form2' : DEL_DRIVER_form}
    return render(request, 'Dalnoboy/drivers.html', context)

def showTripsPage(request):
    if request.method == 'POST':
        ADD_TRIP_form = forms.TripForm(request.POST)
        DEL_TRIP_form = forms.DeleteTripForm(request.POST)
        if ADD_TRIP_form.is_valid():
            ADD_TRIP_form.save()
            return redirect('trips')
        if DEL_TRIP_form.is_valid():
            trip_id = DEL_TRIP_form.cleaned_data['trip_id']
            trip = Trip.objects.get(pk=trip_id)
            trip.delete()
            return redirect('trips')
    else:
        ADD_TRIP_form = forms.TripForm()
        DEL_TRIP_form = forms.DeleteTripForm()

    trips = Trip.objects.all()
    context = {'trips': trips,
               'form1': ADD_TRIP_form,
               'form2' : DEL_TRIP_form}
    return render(request, 'Dalnoboy/trips.html', context)