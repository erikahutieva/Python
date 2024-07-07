# Generated by Django 5.0.4 on 2024-05-04 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylaba', '0004_category_slug_alter_products_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mylaba.products')),
            ],
        ),
    ]
