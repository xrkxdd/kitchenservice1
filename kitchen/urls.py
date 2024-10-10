from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomeView, CustomLoginView, IngredientListView, IngredientCreateView, RecipeCreateView,
    RecipeListView, ChefListView, ChefCreateView, DishTypeListView, DishTypeCreateView,
    ChefDeleteView, IngredientDeleteView, RecipeDeleteView, DishTypeDeleteView
)

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),  # Login page
    path('home/', HomeView.as_view(), name='home'),  # Home page
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page (alternative URL)
    path('logout/', LogoutView.as_view(), name='logout'),  # URL for logging out

    # Dishes (recipes) related URLs
    path('home/dishes/', RecipeListView.as_view(), name='dishes'),  # View list of dishes
    path('dishes/create/', RecipeCreateView.as_view(), name='dishes_create'),  # Create a new dish
    path('home/dishes/delete/<int:pk>/', RecipeDeleteView.as_view(), name='recipe_delete'),

    # Cooks (chefs) related URLs
    path('home/cooks/', ChefListView.as_view(), name='cooks'),  # View list of cooks
    path('home/cooks_create/', ChefCreateView.as_view(), name='cooks_create'),  # Create a new cook
    path('home/cooks/delete/<int:pk>/', ChefDeleteView.as_view(), name='chef_delete'),  # Delete a specific cook by ID

    # Ingredients related URLs
    path('home/ingredients/', IngredientListView.as_view(), name='ingredients'),  # View list of ingredients
    path('home/ingredients_create/', IngredientCreateView.as_view(), name='ingredient_create'),  # Create a new ingredient
    path('home/ingredients/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient_delete'),  # Delete a specific ingredient by ID

    # Dish types related URLs
    path('home/dishtype/', DishTypeListView.as_view(), name='dishtype'),  # View list of dish types
    path('home/dishtype_create/', DishTypeCreateView.as_view(), name='dishtype_create'),  # Create a new dish type
    path('home/dishtype/delete/<int:pk>/', DishTypeDeleteView.as_view(), name='dishtype_delete'),  # Delete a specific dish type by ID
]
