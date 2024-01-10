from django.shortcuts import get_object_or_404, render
from .models import Recipe


def index(request):
    latest_recipe_list = Recipe.objects.order_by('name')[:5]
    context = {"latest_recipe_list": latest_recipe_list}
    return render(request, "recipe/index.html", context)


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, "recipe/detail.html", {"recipe": recipe})
