from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Tag(models.Model):
    title = models.CharField('title', max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    color = models.CharField('color', max_length=8, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(
        'Title',
        max_length=250,
        db_index=True
    )
    measurement_unit = models.CharField('measurement_unit', max_length=20)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Author'
    )
    title = models.CharField('title', max_length=256)
    image = models.ImageField(
        'image',
        help_text='Upload image',
        upload_to='recipes'
    )
    description = models.TextField('description')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='ingredients'
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='tags',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='cooking time'
    )
    pub_date = models.DateTimeField('pub_date', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_recipe'
            )
        ]
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('pub_date',)

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='recipe',
        on_delete=models.CASCADE,
        related_name='ingredient_amounts'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='ingredient',
        on_delete=models.SET_NULL,
        null=True,
        related_name='ingredient_amounts'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='ingredient amount'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = 'Ingredient amount'
        verbose_name_plural = 'Ingredient amounts'

    def __str__(self):
        return f'{self.ingredient.title} - {self.recipe.title}'
