from django.test import TestCase
from recipe.models import Good, GoodIngredient, RecipeIngredient, Recipe, MealPlan, MealPlanEntry
from recipe.measurements import supported_goods
from recipe.page_processors import compile_meal_plan, get_combined_ingredient_list


class RecipeTestCase(TestCase):

    def add_pesto_recipe(self):
        self.pesto_recipe = Recipe.objects.create(
            title="Basil Pesto",
            content="Thoroughly mix all ingredients in a food processor.",
            servings=4.0,
        )
        GoodIngredient.objects.create(recipe=self.pesto_recipe,
                                      good=Good.objects.get(name="pine nuts"),
                                      amount=0.5, unit='cup', prep_method='toasted')
        GoodIngredient.objects.create(recipe=self.pesto_recipe,
                                      good=Good.objects.get(name="lemon"),
                                      amount=2, unit='tablespoon', prep_method='juiced')
        GoodIngredient.objects.create(recipe=self.pesto_recipe,
                                      good=Good.objects.get(name="garlic"),
                                      amount=1, unit='teaspoon', prep_method='crushed')
        GoodIngredient.objects.create(recipe=self.pesto_recipe,
                                      good=Good.objects.get(name="sea salt"),
                                      amount=0.25, unit='teaspoon')
        GoodIngredient.objects.create(recipe=self.pesto_recipe,
                                      good=Good.objects.get(name="black pepper"),
                                      amount=0.25, unit='teaspoon')
        GoodIngredient.objects.create(recipe=self.pesto_recipe,
                                      good=Good.objects.get(name="fresh basil leaves"),
                                      amount=2, unit='cup')
        GoodIngredient.objects.create(recipe=self.pesto_recipe,
                                      good=Good.objects.get(name="extra-virgin olive oil"),
                                      amount=0.25, unit='cup')
        GoodIngredient.objects.create(recipe=self.pesto_recipe,
                                      good=Good.objects.get(name="parmesan cheese"),
                                      amount=0.25, unit='cup', prep_method="shredded")

    def add_pasta_recipe(self):
        self.pasta_recipe = Recipe.objects.create(
            title="Pesto Pasta",
            content="Cook pasta according to instructions. Remove pasta, cook everything else. Combine.",
            servings=1.0,
        )
        GoodIngredient.objects.create(recipe=self.pasta_recipe,
                                      good=Good.objects.get(name="dry penne pasta"),
                                      amount=4, unit='ounce')
        GoodIngredient.objects.create(recipe=self.pasta_recipe,
                                      good=Good.objects.get(name="dried chantarelle"),
                                      amount=2, unit='ounce', prep_method='rehydrated')
        GoodIngredient.objects.create(recipe=self.pasta_recipe,
                                      good=Good.objects.get(name="tomato"),
                                      amount=0.5, unit='cup', prep_method='chopped')
        GoodIngredient.objects.create(recipe=self.pasta_recipe,
                                      good=Good.objects.get(name="extra-virgin olive oil"),
                                      amount=2, unit='tablespoon')
        GoodIngredient.objects.create(recipe=self.pasta_recipe,
                                      good=Good.objects.get(name="butter"),
                                      amount=1, unit='tablespoon')
        RecipeIngredient.objects.create(recipe=self.pasta_recipe,
                                        recipe_ingredient=self.pesto_recipe,
                                        servings=1)

    @staticmethod
    def populate_goods():
        for good in supported_goods:
            Good.objects.create(**good)

    def setUp(self):
        RecipeTestCase.populate_goods()
        self.add_pesto_recipe()
        self.add_pasta_recipe()
        self.meal_plan = MealPlan.objects.create(title="Pesto Week",
                                                 content="Eat pesto all week!")
        MealPlanEntry.objects.create(meal_plan=self.meal_plan,
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
