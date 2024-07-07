from django.shortcuts import render, redirect
from . import models
from . import forms


def success(request):
    return render(request, 'Project/success.html')


def home(request):
    # Получение данных из базы данных
    goods = models.Material.objects.all()

    if request.method == 'POST':
        form = forms.SliderForm(request.POST)
        if form.is_valid():
            # Получаем границы цветов из формы
            LowBlue = form.cleaned_data['LowBlue']
            UpBlue = form.cleaned_data['UpBlue']

            LowGreen = form.cleaned_data['LowGreen']
            UpGreen = form.cleaned_data['UpGreen']

            LowOrange = form.cleaned_data['LowOrange']
            UpOrange = form.cleaned_data['UpOrange']

            LowRed = form.cleaned_data['LowRed']
            UpRed = form.cleaned_data['UpRed']

            even_number = form.cleaned_data['even_number']

            # Prepare the data with coloring
            colored_goods = []
            for good in goods:
                ss_value = int(good.sschet)
                color = get_cell_color(ss_value, LowBlue, UpBlue, LowGreen, UpGreen, LowOrange, UpOrange, LowRed, UpRed, even_number)
                color2 = get_cell_color2(ss_value, even_number)
                colored_goods.append({
                    'code': good.code,
                    'name': good.name,
                    'is_even': good.is_even,
                    'sschet': good.sschet,
                    'color': color,
                    'color2': color2
                })

            context = {
                'selected_goods': colored_goods,
                'form': form
            }

            return render(request, 'Project/colored_table.html', context)
    else:
        form = forms.SliderForm()

    context = {
        'selected_goods': goods,
        'form': form
    }

    return render(request, 'Project/index.html', context)


def get_cell_color(value, LowBlue, UpBlue, LowGreen, UpGreen, LowOrange, UpOrange, LowRed, UpRed, even_number):
    if LowBlue <= value <= UpBlue:
        return "background-color: #130bee;"  # Синий цвет
    elif LowGreen <= value <= UpGreen:
        return "background-color: #29c200;"  # Зеленый цвет
    elif LowOrange <= value <= UpOrange:
        return "background-color: #F8A50A;"  # Оранжевый цвет
    elif LowRed <= value <= UpRed:
        return "background-color: #FF0000;"  # Красный цвет

    else:
        return ""

def get_cell_color2(value, even_number):
    if even_number and value % even_number == 0:
        return "background-color: black;"  # Желтый для кратных