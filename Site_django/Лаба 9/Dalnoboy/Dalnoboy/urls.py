"""Dalnoboy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import CARS_statistics
from . import DRIVERS_statistics

urlpatterns = [
    path('', views.showIndexPage),
    path('cars/', views.showCarsPage, name="cars"),
    path('drivers/', views.showDriversPage, name="drivers"),
    path('trips/', views.showTripsPage, name="trips"),
    path('admin/', admin.site.urls),

    path('cars_statistic/', CARS_statistics.calc_graphic),
    path('drivers_statistic/', DRIVERS_statistics.calc_graphic)
]
