# Generated by Django 5.0.4 on 2024-05-04 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylaba', '0007_cart_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
