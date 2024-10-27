# coursework/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.discipline_list, name='home'),
    path('discipline/<int:discipline_id>/', views.subject_list, name='subject_list'),
    path('subject/<int:subject_id>/teachers/', views.teacher_list, name='teacher_list'),  # Список преподавателей
    path('teacher/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),  # Страница с PDF-файлами
    path('teacher/<int:teacher_id>/upload/', views.upload_pdf, name='upload_pdf'),  # Страница загрузки PDF
]
