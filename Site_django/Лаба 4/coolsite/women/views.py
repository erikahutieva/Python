from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import *
from .models import *
from .utils import *

class WomenHome(DataMixin, ListView):
    """
    Создает класс на основе классов DataMixin и ListView. DataMixin предоставляет вспомогательные методы для работы с данными, а ListView - представление для отображения
    списка объектов.
    """
    model = Women   # Указывает, что это представление будет работать с моделью Women.
    template_name = 'women/index.html'  # Указывает, что это представление будет использовать шаблон women/index.html для отображения списка объектов.
    context_object_name = 'posts'   # Указывает, что объекты модели будут доступны в шаблоне под именем posts.

    def get_context_data(self, *, object_list=None, **kwargs):  # Переопределяет метод родительского класса для подготовки контекстных данных, которые будут переданы в шаблон.
        context = super().get_context_data(**kwargs)    # Вызывает метод get_context_data родительского класса для извлечения контекстных данных по умолчанию.
        c_def = self.get_user_context(title="Главная страница") # В данном случае передается заголовок "Главная страница".
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        # Возвращает набор объектов модели Women, которые отмечены как опубликованные (is_published=True).
        return Women.objects.filter(is_published=True)


# def index(request):
#     posts = Women.objects.all()-
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)

def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})




class AddPage(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True  # Поднять исключение, если доступ запрещен

    permission_required = 'app_name.can_add_post'  # Замените app_name на имя вашего приложения

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))

    def handle_no_permission(self):
        # Обработка случая, когда доступ запрещен
        if self.raise_exception:
            raise PermissionDenied
        return redirect(self.login_url)

    def handle_no_permission(self):
        # Обработка случая, когда доступ запрещен
        if self.raise_exception:
            raise PermissionDenied
        return redirect(self.login_url)
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

def contact(request):
    return HttpResponse("Обратная связь")

# def login(request):
#     return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_id):
#     posts = Women.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'women/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# Когда из главного окна ты хочешь перейти на вкладку чтоб залогиниться:
class LoginUser(DataMixin, LoginView):  # path('login/'
    template_name = 'women/login.html'  # Путь к шаблону, который будет использоваться для отображения формы входа. В данном случае это women/login.html.
    form_class = LoginUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Переопределяет метод родительского класса. Извлекает контекстные данные, относящиеся к пользователю, с помощью метода get_user_context(), и добавляет
        их к контекстным данным, унаследованным от родительского класса.
        """
        context = super().get_context_data(**kwargs)    # Эта строка вызывает метод get_context_data родительского класса (LoginView). Он извлекает контекстные данные по умолчанию, необходимые для отображения формы входа.
        c_def = self.get_user_context(title="Авторизация")  # Эта строка вызывает метод get_user_context класса DataMixin для извлечения контекстных данных, относящихся к пользователю. В данном случае передается заголовок "Авторизация".
        return dict(list(context.items()) + list(c_def.items()))    # Эта строка объединяет контекстные данные из родительского класса и контекстные данные, относящиеся к пользователю, в один словарь и возвращает его.
    
    def get_success_url(self):
        #Переопределяет метод родительского класса. Возвращает URL, на который пользователь будет перенаправлен после успешного входа. В данном случае это
        #home, которое сопоставлено с другим представлением.
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')




