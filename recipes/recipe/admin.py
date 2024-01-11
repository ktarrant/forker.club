from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from recipe.models import Recipe, Good, RecipeIngredient, GoodIngredient


class GoodIngredientInline(admin.TabularInline):
    model = GoodIngredient
    fk_name = "recipe"
    extra = 3  # how many rows to show


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    fk_name = "recipe"
    extra = 1  # how many rows to show


class RecipeAdmin(admin.ModelAdmin):
    inlines = (GoodIngredientInline, RecipeIngredientInline, )


admin.site.register(Good)
admin.site.register(Recipe, RecipeAdmin)
