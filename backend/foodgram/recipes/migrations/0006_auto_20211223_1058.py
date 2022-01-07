# Generated by Django 2.2.16 on 2021-12-23 10:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_auto_20211214_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_shopping_cart', models.BooleanField(default=False, verbose_name='in shopping cart')),
                ('is_favorite', models.BooleanField(default=False, verbose_name='is favorite')),
                ('add_to_favorite', models.DateTimeField(auto_now_add=True, verbose_name='add to favorite')),
                ('add_to_shopping_cart', models.DateTimeField(auto_now_add=True, verbose_name='add to shopping cart')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_favourites', to='recipes.Recipe', verbose_name='recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Favorites',
                'verbose_name_plural': 'Favorites',
                'ordering': ['-add_to_favorite', '-add_to_shopping_cart'],
            },
        ),
        migrations.AddConstraint(
            model_name='favouriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite_recipe'),
        ),
    ]