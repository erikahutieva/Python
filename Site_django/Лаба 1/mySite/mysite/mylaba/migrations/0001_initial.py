# Generated by Django 5.0.4 on 2024-04-05 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('age', models.PositiveSmallIntegerField()),
                ('total_purchase', models.PositiveIntegerField()),
                ('account', models.PositiveIntegerField()),
                ('loan_limit', models.PositiveIntegerField()),
                ('loan_balance', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='')),
                ('price', models.PositiveIntegerField()),
                ('total_amount', models.PositiveIntegerField()),
            ],
        ),
    ]
