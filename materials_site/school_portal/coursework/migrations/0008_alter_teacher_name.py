# Generated by Django 5.1.1 on 2024-09-26 10:41

import coursework.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursework', '0007_delete_subjectteacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=200, verbose_name=coursework.models.Subject),
        ),
    ]
