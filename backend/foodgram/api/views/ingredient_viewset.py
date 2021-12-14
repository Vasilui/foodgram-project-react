from api.permissions import AdminOrReadOnly
from api import serializers
from rest_framework import filters
from api.mixins import ListRetrieveMixin
from recipes.models import Ingredient


class IngredientViewSet(ListRetrieveMixin):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title',)
    ordering = ('title',)
