# Generated by Django 2.2.16 on 2021-12-14 09:40

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20211213_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', max_length=18, samples=None),
        ),
    ]
