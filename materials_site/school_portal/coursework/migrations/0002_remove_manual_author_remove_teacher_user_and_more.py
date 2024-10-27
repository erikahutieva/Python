# Generated by Django 4.1 on 2024-09-19 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursework', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manual',
            name='author',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
        migrations.AddField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursework',
            name='student',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='homework',
            name='student',
            field=models.CharField(max_length=100),
        ),
    ]
