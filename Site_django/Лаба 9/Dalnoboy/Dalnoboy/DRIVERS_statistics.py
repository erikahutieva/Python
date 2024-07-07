from django.shortcuts import render
import matplotlib.pyplot as plt
from matplotlib import use
use("Agg")
from io import BytesIO
import base64
import os
from . import settings
from . import models


def generate_graphic():
    # Получение данных из модели Driver
    drivers = models.Driver.objects.all()
    names = [d.name for d in drivers]
    mileages = [d.total_mileage for d in drivers]

    # Вычисление среднего значения пробега
    if mileages:
        average_mileage = sum(mileages) / len(mileages)
    else:
        average_mileage = 0  # Если нет данных, среднее значение 0

    # Создание графика
    plt.figure(figsize=(10, 6))
    plt.bar(names, mileages)
    plt.xlabel('Водитель')
    plt.ylabel('км')
    plt.title('Общий пробег')

    # Добавление линии среднего значения
    plt.axhline(y=average_mileage, color='r', linestyle='--', label=f'Среднее значение: {average_mileage:.2f} км')
    plt.legend()

    # Сохранение графика в памяти в формате PNG
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Формируем путь к папке для сохранения изображения
    image_dir = os.path.join(settings.BASE_DIR, 'output_graphics')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Формируем полный путь к файлу изображения
    image_path = os.path.join(image_dir, 'drivers_graphic.png')

    # Сохранение графика в формате PNG
    plt.savefig(image_path)
    plt.close()

    return buffer


def calc_graphic(request):
    # Генерация графика
    buffer = generate_graphic()

    # Кодирование изображения в base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Передача изображения в контекст шаблона
    context = {'car_graphic': image_base64}

    # Отображение шаблона с графиком
    return render(request, 'Dalnoboy/drivers_graphic.html', context)
