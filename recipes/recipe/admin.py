from copy import deepcopy

from django.contrib import admin
from recipe.models import Recipe, Good, MealPlan, RecipeGallery


class GoodIngredientInline(admin.TabularInline):
    # TODO: Use special UnitField validation
    model = Recipe.good_ingredients.through
    fk_name = "recipe"
    extra = 3  # how many rows to show


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.recipe_ingredients.through
    fk_name = "recipe"
    extra = 1  # how many rows to show


class RecipeAdmin(admin.ModelAdmin):
    inlines = (GoodIngredientInline, RecipeIngredientInline)
    exclude = ('good_ingredients', 'recipe_ingredients')


class MealPlanEntryInline(admin.TabularInline):
    model = MealPlan.mealplan_entries.through
    fk_name = "mealplan"
    extra = 3  # how many rows to show


class MealPlanAdmin(admin.ModelAdmin):
    inlines = (MealPlanEntryInline, )
    exclude = ('mealplan_entries', )


# TODO: Use special UnitField validation
admin.site.register(Good)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(MealPlan, MealPlanAdmin)
admin.site.register(RecipeGallery)
