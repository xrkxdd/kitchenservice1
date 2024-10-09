from django.urls import path
from . import views
from .views import dishes_create
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login, name='login'),  # Login page
    path('home/', views.home, name='home'),  # Home page
    path('login/', views.login, name='login'),  # Login page (alternative URL)
    path('logout/', LogoutView.as_view(), name='logout'),  # URL for logging out
    path('home/dishes/', views.dishes, name='dishes'),  # View list of dishes
    path('dishes/create/', dishes_create, name='dishes_create'),  # Create a new dish
    path('home/cooks/', views.cooks, name='cooks'),  # View list of cooks
    path('home/ingredients/', views.ingredients, name='ingredients'),  # View list of ingredients
    path('home/ingredients_create/', views.ingredient_create, name='ingredient_create'),  # Create a new ingredient
    path('home/cooks_create/', views.cooks_create, name='cooks_create'),  # Create a new cook
    path('home/dishtype/', views.dishtypes, name='dishtype'),  # View list of dish types
    path('home/dishtype_create/', views.dishtypes_create, name='dishtype_create'),  # Create a new dish type
    path('home/cooks/delete/<int:pk>/', views.chef_delete, name='chef_delete'),  # Delete a specific cook by ID
    path('home/ingredients/delete/<int:pk>/', views.ingredient_delete, name='ingredient_delete'),  # Delete a specific ingredient by ID
    path('home/dishes/delete/<int:pk>/', views.recipe_delete, name='recipe_delete'),  # Delete a specific dish (recipe) by ID
    path('home/dishtype/delete/<int:pk>/', views.dishtype_delete, name='dishtype_delete'),  # Delete a specific dish type by ID
]

