# Generated by Django 2.2.16 on 2021-12-24 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20211223_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favouriterecipe',
            name='add_to_shopping_cart',
            field=models.DateTimeField(verbose_name='add to shopping cart'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Upload image', upload_to='recipes/', verbose_name='image'),
        ),
    ]
