from django.db import models


class Good(models.Model):
    name = models.CharField(max_length=100)
    package = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class GoodIngredient(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=32)
    prep_method = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.amount} {self.unit} {self.good} {self.prep_method}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    multiple = models.FloatField()

    def __str__(self):
        return f"{self.multiple} x {self.recipe.name}"


class Ingredient(models.Model):
    good_ingredient = models.ForeignKey(GoodIngredient,
                                        on_delete=models.CASCADE,
                                        blank=True, null=True)
    recipe_ingredient = models.ForeignKey(RecipeIngredient,
                                          on_delete=models.CASCADE,
                                          blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_thing1_or_thing2",
                check=(
                        models.Q(good_ingredient__isnull=True, recipe_ingredient__isnull=False)
                        | models.Q(good_ingredient__isnull=False, recipe_ingredient__isnull=True)
                ),
            )
        ]

    def __str__(self):
        if self.good_ingredient is not None:
            return str(self.good_ingredient)
        if self.recipe_ingredient is not None:
            return str(self.recipe_ingredient)
        return ""


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField(max_length=1000)
    servings = models.FloatField()
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name
