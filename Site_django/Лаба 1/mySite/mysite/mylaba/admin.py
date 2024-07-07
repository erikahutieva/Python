from django.contrib import admin
from .models import *

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'age')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'surname')
    list_filter = ('id', 'name', 'surname', 'age')
    # list_editable = ('name',)

admin.site.register(Clients, ClientsAdmin)
admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Cart)