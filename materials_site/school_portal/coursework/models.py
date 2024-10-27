from django.db import models

class Discipline(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=200)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
class PDFFile(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    custom_name = models.CharField(max_length=200, blank=True)  # Новое поле для пользовательского названия

    def __str__(self):
        return self.custom_name if self.custom_name else self.file.name  # Показывать пользовательское название или имя файла






class PDFFile(models.Model):
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
