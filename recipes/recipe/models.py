from typing import List
from django.db import models
from django.utils.translation import gettext_lazy
from mezzanine.pages.models import Page, RichText


class Good(models.Model):
    name = models.CharField(max_length=100)
    package = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class GoodIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=32)
    prep_method = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.amount} {self.unit} {self.good} {self.prep_method}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    recipe_ingredient = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                                          related_name='recipe_ingredient')
    amount = models.FloatField()

    def __str__(self):
        return f"{self.amount} servings {self.recipe_ingredient.title}"


class Recipe(Page, RichText):
    servings = models.FloatField()
    good_ingredients = models.ManyToManyField(Good, through=GoodIngredient)
    recipe_ingredients = models.ManyToManyField("Recipe", through=RecipeIngredient)

    class Meta:
        verbose_name = gettext_lazy("Recipe")
        verbose_name_plural = gettext_lazy("Recipes")

    def get_good_ingredients(self) -> List[GoodIngredient]:
        return GoodIngredient.objects.select_related().filter(recipe=self.id)

    def get_recipe_ingredients(self) -> List[GoodIngredient]:
        return RecipeIngredient.objects.select_related().filter(recipe=self.id)

    def get_combined_good_ingredients(self):
        ingredients = list(self.get_good_ingredients())
        for recipe_ingredient in self.get_recipe_ingredients():
            add_ingredients = list(recipe_ingredient.recipe_ingredient.get_combined_good_ingredients())
            multiplier = recipe_ingredient.amount / recipe_ingredient.recipe_ingredient.servings
            for ingredient in add_ingredients:
                ingredient.amount *= multiplier
            ingredients += add_ingredients
        return ingredients
