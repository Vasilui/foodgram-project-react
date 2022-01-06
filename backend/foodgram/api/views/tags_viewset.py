from rest_framework import filters

from api import serializers
from api.mixins import ListRetrieveMixin
from api.permissions import AdminOrReadOnly
from recipes.models import Tag


class TagViewSet(ListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering = ('name',)
