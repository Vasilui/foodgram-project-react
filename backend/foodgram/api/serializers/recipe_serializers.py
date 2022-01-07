from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers

from api.fields import Base64Field
from api.serializers.ingredient_serializer import (IngredientAmountSerializer,
                                                   IngredientWriteSerializer)
from api.serializers.tag_serializers import TagSerializer
from api.serializers.user_serializer import CustomUserSerializer
from api.utils import create_recipe, update_recipe
from recipes.models import Ingredient, Recipe, Tag


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
    name = serializers.CharField(max_length=150)
    text = serializers.CharField(max_length=1000)
    cooking_time = serializers.IntegerField()
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
        new_instance = update_recipe(validated_data, instance)
        super(RecipeWriteSerializer, self).update(new_instance, validated_data)
        new_instance.save()
        return new_instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data

    def validate(self, data):
        ingredients = data.get('ingredients')
        tags = data.get('tags')
        ingredients_id = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_id) != len(set(ingredients_id)):
            raise exceptions.ValidationError(
                'Ингредиенты в рецепте не должны повторяться'
            )
        if len(tags) != len(set(tags)):
            raise exceptions.ValidationError(
                'Теги в рецепте не должны повторяться'
            )
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            if not amount:
                raise exceptions.ValidationError(
                    'У каждого интгредиента должно быть указано количество.'
                )
            if amount <= 0:
                raise exceptions.ValidationError(
                    'Количество ингредиентов должно быть положительным.'
                )
            get_object_or_404(Ingredient, id=ingredient.get('id'))
        return data

    class Meta:
        model = Recipe
        fields = '__all__'
