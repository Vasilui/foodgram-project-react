# Generated by Django 2.2.16 on 2022-01-11 01:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20220107_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]
