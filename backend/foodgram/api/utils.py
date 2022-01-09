from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import FavouriteRecipe


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
