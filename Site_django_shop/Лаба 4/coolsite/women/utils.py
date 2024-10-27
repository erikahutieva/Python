from django.db.models import Count
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]


class PermissionRequiredMixin(UserPassesTestMixin):
    permission_required = ''

    def test_func(self):
        user = self.request.user
        return user.has_perm(self.permission_required)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied
        return redirect('home')

class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
