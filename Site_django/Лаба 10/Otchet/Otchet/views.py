from django.shortcuts import render, redirect

from . import models
from . import forms
from datetime import datetime, date

def home(request):
    global goods, date_start, date_end
    goods = models.Goods.objects.all()

    date_start = date.today()
    date_end = date.today()

    total_price = 0
    success = False

    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            date_start = form.cleaned_data.get('start_date')
            date_end = form.cleaned_data.get('end_date')

            if date_start and date_end:
                date_start_obj = datetime.strptime(str(date_start), "%Y-%m-%d").date()
                date_end_obj = datetime.strptime(str(date_end), "%Y-%m-%d").date()

                goods = models.Goods.objects.filter(date__range=(date_start_obj, date_end_obj))

                for good in goods:
                    total_price += good.price
                
                success = True
    
    context = {
        'selected_goods': goods,
        'form': forms.OrderForm(),
        'success': success,
        'start_date': date_start,
        'end_date': date_end,
        'alert': f"Выбраны записи в промежутке с {date_start} по {date_end}",
        'total_price': f'Общая сумма: {total_price}'
     }
    
    return render(request, 'Otchet/index.html', context)