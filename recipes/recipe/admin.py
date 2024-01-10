from django.contrib import admin

from .models import Recipe, Good, Ingredient

admin.site.register(Good)
admin.site.register(Ingredient)
admin.site.register(Recipe)
