from django.test import TestCase
from mezzanine.pages.models import Page
from recipe.models import Good, GoodIngredient, RecipeIngredient, Recipe, MealPlan, MealPlanEntry
from recipe.measurements import supported_goods
from recipe.page_processors import compile_meal_plan, get_combined_ingredient_list


def add_supported_goods():
    for good in supported_goods:
        Good.objects.create(**good)


def add_pesto_recipe():
    pesto_recipe = Recipe.objects.create(
        title="Basil Pesto",
        content="Thoroughly mix all ingredients in a food processor.",
        servings=4.0,
    )
    GoodIngredient.objects.create(recipe=pesto_recipe,
                                  good=Good.objects.get(name="pine nuts"),
                                  amount=0.5, unit='cup', prep_method='toasted')
    GoodIngredient.objects.create(recipe=pesto_recipe,
                                  good=Good.objects.get(name="lemon"),
                                  amount=2, unit='tablespoon', prep_method='juiced')
    GoodIngredient.objects.create(recipe=pesto_recipe,
                                  good=Good.objects.get(name="garlic"),
                                  amount=1, unit='teaspoon', prep_method='crushed')
    GoodIngredient.objects.create(recipe=pesto_recipe,
                                  good=Good.objects.get(name="sea salt"),
                                  amount=0.25, unit='teaspoon')
    GoodIngredient.objects.create(recipe=pesto_recipe,
                                  good=Good.objects.get(name="black pepper"),
                                  amount=0.25, unit='teaspoon')
    GoodIngredient.objects.create(recipe=pesto_recipe,
                                  good=Good.objects.get(name="fresh basil leaves"),
                                  amount=2, unit='cup')
    GoodIngredient.objects.create(recipe=pesto_recipe,
                                  good=Good.objects.get(name="extra-virgin olive oil"),
                                  amount=0.25, unit='cup')
    GoodIngredient.objects.create(recipe=pesto_recipe,
                                  good=Good.objects.get(name="parmesan cheese"),
                                  amount=0.25, unit='cup', prep_method="shredded")
    return pesto_recipe


def add_pasta_recipe(pesto_recipe):
    pasta_recipe = Recipe.objects.create(
        title="Pesto Pasta",
        content="Cook pasta according to instructions. Remove pasta, cook everything else. Combine.",
        servings=1.0,
    )
    GoodIngredient.objects.create(recipe=pasta_recipe,
                                  good=Good.objects.get(name="dry penne pasta"),
                                  amount=4, unit='ounce')
    GoodIngredient.objects.create(recipe=pasta_recipe,
                                  good=Good.objects.get(name="dried chantarelle"),
                                  amount=2, unit='ounce', prep_method='rehydrated')
    GoodIngredient.objects.create(recipe=pasta_recipe,
                                  good=Good.objects.get(name="tomato"),
                                  amount=0.5, unit='cup', prep_method='chopped')
    GoodIngredient.objects.create(recipe=pasta_recipe,
                                  good=Good.objects.get(name="extra-virgin olive oil"),
                                  amount=2, unit='tablespoon')
    GoodIngredient.objects.create(recipe=pasta_recipe,
                                  good=Good.objects.get(name="butter"),
                                  amount=1, unit='tablespoon')
    RecipeIngredient.objects.create(recipe=pasta_recipe,
                                    recipe_ingredient=pesto_recipe,
                                    servings=1)
    return pasta_recipe


def add_sample_recipes():
    pesto_recipe = add_pesto_recipe()
    return add_pasta_recipe(pesto_recipe)


def add_sample_mealplan(*recipes):
    mealplan = MealPlan.objects.create(title="Sample Mealplan")
    for recipe in recipes:
        MealPlanEntry.objects.create(mealplan=mealplan,
                                     recipe=recipe,
                                     servings=1)


def add_sample_data():
    add_supported_goods()
    recipe = add_sample_recipes()
    add_sample_mealplan(recipe)


class RecipeTestCase(TestCase):
    def setUp(self):
        add_supported_goods()
        self.pesto_recipe = add_pesto_recipe()
        self.pasta_recipe = add_pasta_recipe(self.pesto_recipe)
        self.meal_plan = MealPlan.objects.create(title="Pesto Week",
                                                 content="Eat pesto all week!")
        MealPlanEntry.objects.create(mealplan=self.meal_plan,
                                     recipe=self.pasta_recipe,
                                     servings=1)

    def test_get_goods(self):
        """Animals that can speak are correctly identified"""
        lemon = Good.objects.get(name="lemon")
        evoo = Good.objects.get(name="extra-virgin olive oil")
        self.assertEqual(lemon.volume_unit, "tablespoon")
        self.assertEqual(evoo.volume_quantity, 16.0)

    def test_get_good_ingredients(self):
        """ Query good ingredients of a recipe """
        ingredients = self.pesto_recipe.get_good_ingredients()
        self.assertGreater(len(ingredients), 0)

    def test_get_recipe_ingredients(self):
        """ Query recipe ingredients of a recipe """
        recipe_ingredients = self.pasta_recipe.get_recipe_ingredients()
        self.assertGreater(len(recipe_ingredients), 0)
        ingredient = recipe_ingredients[0]
        self.assertEqual(ingredient.recipe_ingredient.title, self.pesto_recipe.title)
        self.assertEqual(ingredient.servings, 1.0)

    def test_compile_meal_plan(self):
        """ Test compile_meal_plan from page_processors """
        recipes = compile_meal_plan(self.meal_plan)
        self.assertGreater(len(recipes), 0)

    def test_combined_ingredient_list(self):
        recipes = compile_meal_plan(self.meal_plan)
        combined_ingredient_list = get_combined_ingredient_list(recipes)
        self.assertGreater(len(combined_ingredient_list), 0)

    def test_recipe_search_title(self):
        query = "pesto"
        results = Page.objects.search(query)
        self.assertGreater(len(results), 0)

    def test_recipe_search_ingredient(self):
        query = "pine nuts"
        results = Recipe.objects.search(query)
        self.assertGreater(len(results), 0)

    def test_recipe_search_ingredient_via_page(self):
        query = "pine nuts"
        results = Page.objects.search(query, search_fields=('recipe__good_ingredients__name', ))
        self.assertGreater(len(results), 0)

    def test_mealplan_search(self):
        query = "pesto"
        results = MealPlan.objects.search(query)
        self.assertGreater(len(results), 0)
