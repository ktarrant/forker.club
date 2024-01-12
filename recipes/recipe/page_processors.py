from django.shortcuts import render
from mezzanine.pages.page_processors import processor_for
from .models import Recipe, GoodIngredient, RecipeIngredient


@processor_for(Recipe)
def recipe_render(request, page):
    good_ingredient_list = page.recipe.get_good_ingredients()
    recipe_ingredient_list = page.recipe.get_recipe_ingredients()
    context = {"good_ingredient_list": good_ingredient_list,
               "recipe_ingredient_list": recipe_ingredient_list}
    return render(request, "pages/recipe.html", context=context)
