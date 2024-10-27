from django.shortcuts import render, HttpResponse
from math import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import use as pltuse
from datetime import datetime

def create_graphic(formula, min, max):
    filename = ''
    error = 0
    plt.clf()
    try:
        pltuse('SVG')
        x = np.linspace(min, max, 500)
        y = eval(formula)
        plt.plot(x, y)
        plt.title('График функции: ' + formula)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"graph_{current_time}.png"
        plt.savefig(f'myapp/static/myapp/images/{filename}')
        plt.close()

    except Exception as e:
        error = 1

    return (filename, error)
def index(request):
    context = {}
    if request.POST:
        response = request.POST
        filename, error = create_graphic(response['formula'], float(response['min']), float(response['max']))
        context['formula'] = response['formula']
        context['error'] = error
        context['filename'] = 'static/myapp/images/' + filename

    return render(request, 'myapp/index.html', context=context)