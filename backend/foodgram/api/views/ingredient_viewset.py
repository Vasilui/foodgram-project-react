from django_filters import rest_framework
from rest_framework import viewsets

from api import serializers
from api.filters import IngredientFilter
from api.mixins import ListRetrieveMixin
from recipes.models import Ingredient, IngredientAmount


class IngredientViewSet(ListRetrieveMixin):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientReadSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class IngredientAmountViewSet(viewsets.ModelViewSet):
    queryset = IngredientAmount.objects.all()
    serializer_class = serializers.IngredientAmountSerializer
