from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import CustomUser as User
# from users.models import Follow


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'password', 'username', 'first_name', 'last_name')


class CustomUserSerializer(UserSerializer):
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

    # def get_is_subscribed(self, obj):
    #     user = self.context.get('request').user
    #     if user.is_anonymous:
    #         return False
    #     return Follow.objects.filter(user=user, author=obj.id).exists()


# class FollowSerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source='author.id')
#     email = serializers.ReadOnlyField(source='author.email')
#     username = serializers.ReadOnlyField(source='author.username')
#     first_name = serializers.ReadOnlyField(source='author.first_name')
#     last_name = serializers.ReadOnlyField(source='author.last_name')
#     is_subscribed = serializers.SerializerMethodField()
#     recipes = serializers.SerializerMethodField()
#     recipes_count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Follow
#         fields = ('id', 'email', 'username', 'first_name', 'last_name',
#                   'is_subscribed', 'recipes', 'recipes_count')
#
#     def get_is_subscribed(self, obj):
#         return Follow.objects.filter(
#             user=obj.user, author=obj.author
#         ).exists()

    # def get_recipes(self, obj):
    #     request = self.context.get('request')
    #     limit = request.GET.get('recipes_limit')
    #     queryset = Recipe.objects.filter(author=obj.author)
    #     if limit:
    #         queryset = queryset[:int(limit)]
    #     return CropRecipeSerializer(queryset, many=True).data
    #
    # def get_recipes_count(self, obj):
    #     return Recipe.objects.filter(author=obj.author).count()
