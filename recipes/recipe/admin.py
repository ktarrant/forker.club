from django.contrib import admin

from .models import Recipe, Good, RecipeIngredient, GoodIngredient, Ingredient

admin.site.register(Good)
admin.site.register(RecipeIngredient)
admin.site.register(GoodIngredient)
admin.site.register(Ingredient)
admin.site.register(Recipe)
