from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('searchClients', searchClients, name='searchClients'),
    path('searchProducts', searchProducts, name='searchProducts'),
    path('client/<int:clientid>/', client, name='client'),
    path('product/<int:productid>/', product, name='product'),
    path('categories/', categorys, name='categories'),
    path('catalog/<slug:cat_slug>', catalog_category, name='catalog-category'),
    path('cart', cart, name='cart'),
    path('remove_from_cart/<int:item_id>', remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    # path('login/', login, name='login')
]