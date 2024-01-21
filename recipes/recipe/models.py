from typing import List
from django.db import models
from django.utils.translation import gettext_lazy as _
from mezzanine.pages.models import Page, RichText
from mezzanine.generic.fields import CommentsField, RatingField

from recipe.measurements import supported_units

UNIT_CHOICES = [(str(unit), str(unit).replace("_", " "))
                for unit in supported_units]


class Good(models.Model):
    name = models.CharField(max_length=100)
    package = models.CharField(max_length=100)
    weight_quantity = models.FloatField()
    weight_unit = models.CharField(max_length=32, choices=UNIT_CHOICES)
    volume_quantity = models.FloatField()
    volume_unit = models.CharField(max_length=32, choices=UNIT_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Good")
        verbose_name_plural = _("Goods")


class GoodIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=32, choices=UNIT_CHOICES)
    prep_method = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.amount} {self.unit} {self.good} {self.prep_method}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    recipe_ingredient = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                                          related_name='recipe_ingredient')
    servings = models.FloatField()

    def __str__(self):
        return f"{self.servings} servings {self.recipe_ingredient.title}"


class Recipe(Page, RichText):
    servings = models.FloatField()
    good_ingredients = models.ManyToManyField(Good, through=GoodIngredient)
    recipe_ingredients = models.ManyToManyField("Recipe", through=RecipeIngredient)
    rating = RatingField()
    comments = CommentsField()
    search_fields = ('good_ingredients__name', 'recipe_ingredients__title', )

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")

    def get_good_ingredients(self) -> List[GoodIngredient]:
        return GoodIngredient.objects.select_related().filter(recipe=self.id)

    def get_recipe_ingredients(self) -> List[GoodIngredient]:
        return RecipeIngredient.objects.select_related().filter(recipe=self.id)


class MealPlanEntry(models.Model):
    mealplan = models.ForeignKey('MealPlan', on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    servings = models.FloatField()


class MealPlan(Page, RichText):
    mealplan_entries = models.ManyToManyField(Recipe, through=MealPlanEntry)
    comments = CommentsField()
    search_fields = ('mealplan_entries__title', )

    class Meta:
        verbose_name = _("Meal Plan")
        verbose_name_plural = _("Meal Plans")


class MyProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    bio = models.TextField(default="", null="", blank="")
