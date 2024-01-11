from django.shortcuts import render
from mezzanine.pages.page_processors import processor_for
from .models import Recipe, GoodIngredient, RecipeIngredient


@processor_for(Recipe)
def recipe_render(request, page):
    good_ingredient_list = GoodIngredient.objects.select_related().filter(recipe=page.recipe.id)
    recipe_ingredient_list = RecipeIngredient.objects.select_related().filter(recipe=page.recipe.id)
    context = {"good_ingredient_list": good_ingredient_list,
               "recipe_ingredient_list": recipe_ingredient_list}
    return render(request, "pages/recipe.html", context=context)
