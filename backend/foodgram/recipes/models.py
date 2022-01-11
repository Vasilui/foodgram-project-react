from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        unique=True
    )
    slug = models.SlugField(max_length=100, verbose_name='Слаг')
    color = ColorField(default='#FF0000', verbose_name='Цвет')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'slug'),
                name='unique_tag_name_slug'
            )
        ]

        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=250,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='ед. изм.',
        max_length=20
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}({self.measurement_unit})'


class RecipeManage(models.QuerySet):
    def with_tags_and_authors(self):
        return self.select_related('author').prefetch_related(
            'tags', 'ingredients'
        )

    def with_favorite(self, user):
        sub_qs = FavouriteRecipe.objects.filter(
            user=user,
            recipe=models.OuterRef('id'),
            is_favorited=True,
        )
        return self.annotate(is_favorited=models.Exists(sub_qs))

    def with_shopping_cart(self, user):
        sub_qs = FavouriteRecipe.objects.filter(
            user=user,
            recipe=models.OuterRef('id'),
            is_in_shopping_cart=True,
        )
        return self.annotate(is_in_shopping_cart=models.Exists(sub_qs))

    def with_favorite_and_shopping_cart(self, user):
        return self.with_favorite(user=user).with_shopping_cart(user=user)


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(verbose_name='Название', max_length=256)
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Загрузить картинку',
        upload_to='recipes/images/'
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    objects = models.Manager()
    recipe_obj = RecipeManage.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_author_recipe'
            )
        ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('pub_date',)

    def __str__(self):
        return self.name


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='favourite_recipes',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_favourites',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В списке покупок'
    )
    is_favorited = models.BooleanField(verbose_name='Избранное', default=False)
    add_to_favorite = models.DateTimeField(
        verbose_name='Добавить в избранное',
        auto_now_add=True
    )
    add_to_shopping_cart = models.DateTimeField(
        verbose_name='Добавить с список покупок',
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe',
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-add_to_favorite', '-add_to_shopping_cart']

    def __str__(self):
        return f'{self.user} - {self.recipe.name}'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_amounts'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.SET_NULL,
        null=True,
        related_name='ingredient_amounts'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество',
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient} - {self.recipe}'
