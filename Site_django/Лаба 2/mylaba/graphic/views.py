from django.shortcuts import render, redirect
from .models import Points
import matplotlib.pyplot as plt
from matplotlib import use
from datetime import datetime
import numpy as np

use('Agg')
def create_graphic(x_min='', x_max='', y_min='', y_max=''):
    plt.clf()

    points = Points.objects.all()
    if x_min != '':
        points = points.filter(x__gte=x_min)
    if x_max != '':
        points = points.filter(x__lte=x_max)
    if y_min != '':
        points = points.filter(y__gte=y_min)
    if y_max != '':
        points = points.filter(y__lte=y_max)

    pnts = []
    xs = []
    ys = []

    if points:
        for point in points:
            if [point.x, point.y] in pnts:
                continue
            else:
                pnts.append([point.x, point.y])

    pnts = sorted(pnts)
    for pnt in pnts:
        xs.append(pnt[0])
        ys.append(pnt[1])

    # Вычисление среднего значения y
    if ys:
        y_mean = sum(ys) / len(ys)
        y_max = max(ys)
        x_max = xs[ys.index(y_max)]
    else:
        y_mean = 0  # Если нет точек, среднее значение 0
        y_max = 0
        x_max = 0

    plt.plot(xs, ys, label='Данные')
    plt.axhline(y=y_mean, color='r', linestyle='--', label=f'Среднее значение: {y_mean:.2f}')
    plt.scatter(x_max, y_max, color='b', s=100, zorder=5, label=f'Максимальное значение: {y_max:.2f}')
    plt.title('График')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.legend()

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"graph_{current_time}.png"
    plt.savefig(f'graphic/static/graphic/images/{filename}')
    plt.close()

    return filename


def create_histogram():
    plt.clf()

    points = Points.objects.all()
    xs = [point.x for point in points]
    ys = [point.y for point in points]

    plt.hist(ys, bins=10, alpha=0.7, label='Y values')
    if ys:
        y_mean = sum(ys) / len(ys)
        plt.axvline(y_mean, color='r', linestyle='--', label=f'Среднее значение: {y_mean:.2f}')

    plt.title('Гистограмма Y значений')
    plt.xlabel('Y')
    plt.ylabel('Частота')
    plt.legend()

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"histogram_{current_time}.png"
    plt.savefig(f'graphic/static/graphic/images/{filename}')
    plt.close()

    return filename


def create_pie_chart():
    plt.clf()

    points = Points.objects.all()
    ys = [point.y for point in points]
    unique_ys, counts = np.unique(ys, return_counts=True)

    plt.pie(counts, labels=unique_ys, autopct='%1.1f%%')
    plt.title('Круговая диаграмма Y значений')

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"pie_chart_{current_time}.png"
    plt.savefig(f'graphic/static/graphic/images/{filename}')
    plt.close()

    return filename


def index(request):
    context = {
        'title': 'Главная страница',
        'img_url': '',
        'hist_url': '',
        'pie_url': '',
        'points': Points.objects.all()
    }

    if request.POST:
        if 'x' in request.POST:
            x = float(request.POST['x'])
            y = float(request.POST['y'])

            x_min = ''
            x_max = ''
            y_min = ''
            y_max = ''

            Points.objects.create(x=x, y=y)
        else:
            x_min = request.POST['x_min']
            x_max = request.POST['x_max']
            y_min = request.POST['y_min']
            y_max = request.POST['y_max']

        context['img_url'] = 'static/graphic/images/' + create_graphic(x_min, x_max, y_min, y_max)
        context['hist_url'] = 'static/graphic/images/' + create_histogram()
        context['pie_url'] = 'static/graphic/images/' + create_pie_chart()

    return render(request, 'graphic/index.html', context=context)


def clear_graphic(request):
    Points.objects.all().delete()
    return redirect('home')
