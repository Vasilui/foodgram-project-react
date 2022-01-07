from django.contrib import admin

from .models import FavouriteRecipe, Ingredient, IngredientAmount, Recipe, Tag

admin.site.register(FavouriteRecipe)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'text',
        'get_tags',
        'favorites',
        'pub_date',
        'image',
        'cooking_time',
    )
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    ordering = ('pub_date', 'author')

    def favorites(self, obj):
        if count := obj.in_favourites.count():
            return count
        return None
    favorites.short_description = 'Избранное'

    def get_tags(self, obj):
        if tags := obj.tags.values_list('name', flat=True):
            return list(tags)
        return None
    get_tags.short_description = 'Теги'
