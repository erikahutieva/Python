from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from . import settings
from . import models

from matplotlib import use
use("Agg")
def generate_graphic():
    # Получение данных из модели Car
    cars = models.Car.objects.all()
    brands = [car.brand for car in cars]
    mileages = [car.mileage for car in cars]

    # Вычисление среднего значения пробега
    if mileages:
        average_mileage = sum(mileages) / len(mileages)
    else:
        average_mileage = 0  # Если нет данных, среднее значение 0

    # Создание графика
    plt.figure(figsize=(10, 6))
    plt.bar(brands, mileages)
    plt.xlabel('Марка автомобиля')
    plt.ylabel('Пробег')
    plt.title('Пробег автомобилей по маркам')

    # Добавление линии среднего значения
    plt.axhline(y=average_mileage, color='r', linestyle='--', label=f'Среднее значение: {average_mileage:.2f}')
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
    image_path = os.path.join(image_dir, 'cars_graphic.png')

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
    return render(request, 'Dalnoboy/cars_graphic.html', context)
