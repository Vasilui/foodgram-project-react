from .models import Recipe, Ingredient, Tag
from django.contrib import admin


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'slug')
    search_fields = ('title', 'slug')
    list_filter = ('title', 'color',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'description',
        'pub_date',
        'image',
        'cooking_time'
    )
    search_fields = ('author', 'title')
    list_filter = ('author', 'title', 'tag', 'cooking_time')
    ordering = ('pub_date', 'author')
