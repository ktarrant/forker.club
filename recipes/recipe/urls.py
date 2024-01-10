from django.urls import path

from . import views

urlpatterns = [
    # ex: /recipe/
    path("", views.index, name="index"),
    # ex: /recipe/5/
    path("<int:recipe_id>/", views.detail, name="detail"),
]
