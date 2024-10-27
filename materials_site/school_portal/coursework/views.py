from django.shortcuts import render, get_object_or_404, redirect
from .models import Discipline, Subject, Teacher, PDFFile
from .forms import PDFUploadForm

# Отображение списка преподавателей по выбранному предмету
def teacher_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject_teachers = Teacher.objects.filter(subject=subject)
    return render(request, 'teachers_list.html', {'subject': subject, 'teachers': subject_teachers})

# Получение списка дисциплин
def discipline_list(request):
    disciplines = Discipline.objects.all()
    return render(request, 'home.html', {'disciplines': disciplines})

# Отображение списка предметов по выбранной дисциплине
def subject_list(request, discipline_id):
    discipline = get_object_or_404(Discipline, id=discipline_id)
    subjects = Subject.objects.filter(discipline=discipline)
    return render(request, 'subject_list.html', {'discipline': discipline, 'subjects': subjects})

# Страница учителя с загруженными PDF-файлами
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    pdf_files = PDFFile.objects.filter(teacher=teacher)
    return render(request, 'teacher_detail.html', {'teacher': teacher, 'pdf_files': pdf_files})
def upload_pdf(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)  # Получаем преподавателя по его ID
    pdf_files = PDFFile.objects.filter(teacher=teacher)  # Получаем PDF-файлы, связанные с данным преподавателем

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.save(commit=False)  # Не сохраняем сразу, чтобы добавить связь с преподавателем
            pdf_file.teacher = teacher  # Связываем файл с преподавателем
            pdf_file.save()  # Сохраняем файл в базу данных
            return redirect('upload_pdf', teacher_id=teacher_id)  # Перенаправляем на ту же страницу для обновления списка файлов
    else:
        form = PDFUploadForm()

    return render(request, 'upload_pdf.html', {'teacher': teacher, 'files': pdf_files, 'form': form})




