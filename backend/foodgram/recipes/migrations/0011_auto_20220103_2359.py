# Generated by Django 2.2.16 on 2022-01-03 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20220102_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favouriterecipe',
            name='add_to_shopping_cart',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Добавить с список покупок'),
        ),
    ]
