from django.db import models
from django.utils.translation import gettext_lazy
from mezzanine.pages.models import Page, RichText


class Good(models.Model):
    name = models.CharField(max_length=100)
    package = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Recipe(Page, RichText):
    servings = models.FloatField()
    good_ingredients = models.ManyToManyField(Good, through="GoodIngredient",)
    recipe_ingredients = models.ManyToManyField("Recipe", through="RecipeIngredient")

    class Meta:
        verbose_name = gettext_lazy("Recipe")
        verbose_name_plural = gettext_lazy("Recipes")


class GoodIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=32)
    prep_method = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.amount} {self.unit} {self.good} {self.prep_method}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    recipe_ingredient = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                          related_name='recipe_ingredient')
    amount = models.FloatField()

    def __str__(self):
        return f"{self.amount} servings {self.recipe_ingredient.name}"
