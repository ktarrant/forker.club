from copy import deepcopy

from django.contrib import admin
from recipe.models import Recipe, Good


recipe_extra_fieldsets = ((None, {"fields": ("good_ingredients", 'recipe_ingredients')}),)


class GoodIngredientInline(admin.TabularInline):
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


admin.site.register(Good)
admin.site.register(Recipe, RecipeAdmin)
