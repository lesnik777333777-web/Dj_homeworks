from django.urls import path
from . import views

urlpatterns = [
    # <str:recipe_name> захватывает часть адреса (например, 'omlet') и передает в функцию
    path('<str:recipe_name>/', views.show_recipe, name='show_recipe'),
]