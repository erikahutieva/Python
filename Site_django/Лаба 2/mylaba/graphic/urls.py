from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('clear_graphic', clear_graphic, name='clear_graphic')
]
