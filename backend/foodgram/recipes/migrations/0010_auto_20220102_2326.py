# Generated by Django 2.2.16 on 2022-01-02 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20211224_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favouriterecipe',
            old_name='is_favorite',
            new_name='is_favorited',
        ),
    ]
