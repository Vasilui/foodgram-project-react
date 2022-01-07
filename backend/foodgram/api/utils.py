from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status
from rest_framework.response import Response

from recipes.models import FavouriteRecipe, Ingredient, Recipe, Tag


def get_tags(serialized_data):
    tags_data = serialized_data.pop('tags')
    return [get_object_or_404(Tag, id=tag.id) for tag in tags_data]


def add_ingredients(recipe_instance, ingredients):
    for ingredient in ingredients:
        ingredient_obj = get_object_or_404(
            Ingredient, id=ingredient.get('id')
        )
        recipe_instance.ingredients.add(
            ingredient_obj,
            through_defaults={'amount': ingredient.get('amount')}
        )
    return recipe_instance


def create_recipe(serialized_data):
    author = serialized_data.get('author')
    name = serialized_data.get('name')
    if Recipe.objects.filter(author=author, name=name).exists():
        raise exceptions.ValidationError(
            'Рецепт с таким названием уже существует.'
        )
    ingredient_data = serialized_data.pop('ingredients')
    tags = get_tags(serialized_data)

    new_recipe = Recipe.objects.create(**serialized_data)
    new_recipe.tags.add(*tags)
    add_ingredients(new_recipe, ingredient_data)

    new_recipe.save()
    return new_recipe


def update_recipe(serialized_data, recipe_instance):
    tags = get_tags(serialized_data)
    ingredients_data = serialized_data.get('ingredients')

    recipe_instance.tags.clear()
    recipe_instance.ingredients.clear()
    recipe_instance.tags.add(*tags)

    add_ingredients(recipe_instance, ingredients_data)
    return recipe_instance

    # recipe_instance.name = serialized_data.get(
    #     'name', recipe_instance.name
    # )
    # recipe_instance.text = serialized_data.get(
    #     'text', recipe_instance.text
    # )
    # recipe_instance.cooking_time = serialized_data.get(
    #     'cooking_time', recipe_instance.cooking_time
    # )
    # recipe_instance.image = serialized_data.get(
    #     'image', recipe_instance.image
    # )
    # recipe_instance.save()
    # return recipe_instance


def favorite(recipe_view, request, pk):
    user = recipe_view.request.user
    recipe = recipe_view.get_object()
    if request.method == 'GET':
        FavouriteRecipe.objects.update_or_create(
            user=user, recipe=recipe,
            defaults={
                'user': user,
                'recipe': recipe,
                'is_favorited': True
            }
        )
        return Response(
            {'status': 'Рецепт успешно добавлен в избранное'},
            status=status.HTTP_201_CREATED
        )

    fav_recipe = get_object_or_404(
        FavouriteRecipe,
        recipe=recipe, user=user
    )
    if not fav_recipe.is_in_shopping_cart:
        fav_recipe.delete()
    else:
        fav_recipe.is_favorited = False
        fav_recipe.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
