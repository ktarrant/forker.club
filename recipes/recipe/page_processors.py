import pint
from django.shortcuts import render
from mezzanine.pages.page_processors import processor_for
from .models import Recipe, MealPlan, MealPlanEntry


@processor_for(Recipe)
def recipe_render(request, page):
    good_ingredient_list = page.recipe.get_good_ingredients()
    recipe_ingredient_list = page.recipe.get_recipe_ingredients()

    context = {"good_ingredient_list": good_ingredient_list,
               "recipe_ingredient_list": recipe_ingredient_list}
    return render(request, "pages/recipe.html", context=context)


def update_recipe_dict(recipes: dict, add_recipe: dict):
    try:
        existing_recipe = recipes[add_recipe['recipe'].id]
        existing_recipe['servings'] += add_recipe['servings']
    except KeyError:
        recipes[add_recipe['recipe'].id] = add_recipe


def get_combined_recipe_ingredients(recipe_ingredients, multiplier=1.0):
    recipes = {}
    # TODO: This is probably a little wasteful in terms of database queries
    for recipe_ingredient in recipe_ingredients:
        recipe = {
            'recipe': recipe_ingredient.recipe_ingredient,
            'servings': recipe_ingredient.servings * multiplier,
            'recipe_ingredients': recipe_ingredient.recipe_ingredient.get_recipe_ingredients(),
        }
        sub_multiplier = recipe['servings'] / recipe['recipe'].servings

        for add_recipe in get_combined_recipe_ingredients(recipe['recipe_ingredients'],
                                                          sub_multiplier):
            update_recipe_dict(recipes, add_recipe)

        # Safe add the base recipe ingredient
        update_recipe_dict(recipes, recipe)

    return recipes


def compile_meal_plan(mealplan):
    entries = MealPlanEntry.objects.select_related().filter(mealplan=mealplan.id)
    recipes = {}
    for entry in entries:
        multiplier = (entry.servings / entry.recipe.servings)
        # TODO: Danger if a top-level recipe is added that is also a recipe ingredient
        recipe = {
            'recipe': entry.recipe,
            'servings': entry.servings,
            'recipe_ingredients': entry.recipe.get_recipe_ingredients(),
        }

        multiplier = entry.servings / entry.recipe.servings
        combined_recipe_ingredients = get_combined_recipe_ingredients(recipe['recipe_ingredients'],
                                                                      multiplier)

        for add_recipe in combined_recipe_ingredients.values():
            update_recipe_dict(recipes, add_recipe)

        update_recipe_dict(recipes, recipe)

    # Update the recipes dictionary to include properly scaled ingredients
    for recipe in recipes.values():
        ingredients = recipe['recipe'].get_good_ingredients()
        multiplier = recipe['servings'] / recipe['recipe'].servings
        recipe['ingredients'] = [
            {
                "good": ingredient.good,
                "amount": ingredient.amount * multiplier,
                "unit": ingredient.unit,
                "prep_method": ingredient.prep_method,
            }
            for ingredient in ingredients
        ]

    return recipes


def get_combined_ingredient_list(recipes):
    ingredients = {}
    reg = pint.UnitRegistry()
    for recipe in recipes.values():
        for ingredient in recipe['ingredients']:
            good = ingredient['good']
            context_name = good.name.replace(' ', '_')
            if good.id not in ingredients:
                # Have not processed this ingredient before,
                # so we need to build the context for converting it
                wq = reg.Quantity(good.weight_quantity, good.weight_unit)
                lq = reg.Quantity(good.volume_quantity, good.volume_unit)
                context = pint.Context(context_name)
                context.add_transformation('[length] ** 3', '[mass]',
                                           lambda ureg, x: x * wq / lq)
                context.add_transformation('[mass]', '[length] ** 3',
                                           lambda ureg, x: x * lq / wq)
                reg.add_context(context)

            quantity = reg.Quantity(ingredient['amount'], ingredient['unit'])
            try:
                existing_ingredient = ingredients[ingredient['good'].id]
                grocery_unit = existing_ingredient['unit']
                existing_ingredient['amount'] += quantity.to(grocery_unit, context_name).magnitude
            except KeyError:
                grocery_unit = ingredient['good'].weight_unit
                new_ingredient = {
                    "good": ingredient['good'],
                    "amount": quantity.to(grocery_unit, context_name).magnitude,
                    "unit": grocery_unit,
                    "prep_method": ingredient['prep_method'],
                }
                ingredients[ingredient['good'].id] = new_ingredient

    return list(ingredients.values())


@processor_for(MealPlan)
def meal_plan_render(request, page):
    recipes = compile_meal_plan(page.mealplan)
    for recipe_id in recipes:
        recipes[recipe_id]['content'] = recipes[recipe_id]['recipe'].content

    combined_ingredient_list = get_combined_ingredient_list(recipes)

    context = {"recipes": list(recipes.values()),
               "combined_ingredient_list": list(combined_ingredient_list)}
    return render(request, "pages/mealplan.html", context=context)
