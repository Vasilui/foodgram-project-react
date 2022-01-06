from rest_framework import serializers

from api.fields import Base64Field
from api.serializers.ingredient_serializer import (IngredientAmountSerializer,
                                                   IngredientWriteSerializer)
from api.serializers.tag_serializers import TagSerializer
from api.serializers.user_serializer import CustomUserSerializer
from api.utils import create_recipe, update_recipe
from recipes.models import Recipe, Tag


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amounts'
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    image = Base64Field()

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientWriteSerializer(many=True)
    image = Base64Field(max_length=False, use_url=True)
    is_favorited = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return create_recipe(validated_data)

    def update(self, instance, validated_data):
        return update_recipe(validated_data, instance)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data

    class Meta:
        model = Recipe
        fields = '__all__'
