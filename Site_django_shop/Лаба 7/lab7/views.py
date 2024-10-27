from django.shortcuts import render, redirect
from .models import Person
from django.contrib import messages
from django.db.models import Q

def person_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        inn = request.POST.get('inn')

        try:
            person = Person.objects.get(inn=inn)
            messages.error(request, 'Этот ИНН уже используется!')
        except Person.DoesNotExist:
            person = Person(first_name=first_name, last_name=last_name, middle_name=middle_name, inn=inn)
            person.save()
            messages.success(request, 'Новый человек успешно добавлен!')

    people = Person.objects.all()
    context = {'people': people}
    return render(request, 'person.html', context)
def get_inn(request):
    if request.method == 'POST':
        inn = request.POST.get('inn')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')

        # Поиск по ИНН
        people = Person.objects.filter(
            Q(inn=inn)
        )

        if people.exists():
            # Формирование фио
            fio = list((person.first_name + " " + person.last_name + " " + person.middle_name for person in people))

            # Вывод сообщения с перечислением всех найденных ИНН
            message = 'ИНН: {}; ФИО: {}'.format(
                inn,
                fio[0]
            )
            messages.success(request, message)
        else:
            messages.error(request, 'Человек с таким ФИО не найден!')

    return redirect('person_view')

