from django.contrib.auth import get_user_model
from django.db.models import Sum
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django_filters import rest_framework as filters
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from api import serializers
from api.filters import RecipeFilter
from api.mixins import ListRetrieveMixin
from api.paginations import LimitPageNumberPagination
from api.permissions import OwnerOrReadOnly
from api.utils import favorite
from recipes.models import FavouriteRecipe, Recipe

User = get_user_model()


class RecipeViewSet(ListRetrieveMixin):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    ordering = ('-pub_date',)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Recipe.objects.all()
        user = get_object_or_404(User, id=self.request.user.id)
        return Recipe.recipe_obj.with_favorite_and_shopping_cart(user=user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST', 'PATCH']:
            return serializers.RecipeWriteSerializer
        return serializers.RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        return favorite(self, request, pk)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()

        if request.method == 'GET':
            FavouriteRecipe.objects.update_or_create(
                user=user,
                recipe=recipe,
                defaults={
                    'user': user, 'recipe': recipe,
                    'is_in_shopping_cart': True
                },
            )
            return Response(
                {'status': 'Рецепт успешно добавлен в список покупок'},
                status=status.HTTP_201_CREATED
            )

        else:
            fav_recipe = get_object_or_404(
                FavouriteRecipe,
                recipe=recipe,
                user=user
            )
            if not fav_recipe.is_favorited:
                fav_recipe.delete()
            else:
                fav_recipe.is_in_shopping_cart = False
                fav_recipe.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, pk=None):
        user = request.user
        recipes = Recipe.objects.filter(
            in_favourites__user=user,
            in_favourites__is_in_shopping_cart=True
        )
        ingredients = recipes.values(
            'ingredients__name',
            'ingredients__measurement_unit').order_by(
            'ingredients__name').annotate(
            ingredients_total=Sum('ingredient_amounts__amount')
        )
        shopping_list = {}
        for item in ingredients:
            title = item.get('ingredients__name')
            count = str(item.get('ingredients_total')) + ' ' + item[
                'ingredients__measurement_unit'
            ]
            shopping_list[title] = count
        # data = ''
        # for key, value in shopping_list.items():
        #     data += f'{key} - {value}\n'
        # return HttpResponse(data, content_type='text/plain')
        template = get_template("shopping_cart.html")
        return PDFTemplateResponse(
            request=request,
            template=template,
            filename="shopping_cart.pdf",
            context={"shopping_list": shopping_list},
            show_content_in_browser=False,
            cmd_options={'margin-top': 50, },
        )
