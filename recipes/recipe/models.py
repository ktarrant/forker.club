from django.db import models


class Good(models.Model):
    name = models.CharField(max_length=100)
    package = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=32)
    prep_method = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.amount} {self.unit} {self.good} {self.prep_method}"


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField(max_length=1000)
    servings = models.FloatField()
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name
