# Generated by Django 5.0.4 on 2024-05-04 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mylaba', '0005_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product_id',
            new_name='product',
        ),
    ]
