from django.urls import path
from django.contrib import admin
from django.urls import include
from . import views
from .views import (
    HomeView, IngredientListView, IngredientCreateView, RecipeCreateView,
    RecipeListView, ChefListView, ChefCreateView, DishTypeListView, DishTypeCreateView,
    ChefDeleteView, IngredientDeleteView, RecipeDeleteView, DishTypeDeleteView,
    CustomLoginView,
)

app_name = 'kitchen'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),


    path('home/dishes/', RecipeListView.as_view(), name='dishes'),
    path('dishes/create/', RecipeCreateView.as_view(), name='dishes_create'),
    path('home/dishes/delete/<int:pk>/', RecipeDeleteView.as_view(), name='recipe_delete'),

    path('home/cooks/', ChefListView.as_view(), name='cooks'),
    path('home/cooks_create/', ChefCreateView.as_view(), name='cooks_create'),
    path('home/cooks/delete/<int:pk>/', ChefDeleteView.as_view(), name='chef_delete'),


    path('home/ingredients/', IngredientListView.as_view(), name='ingredients'),
    path('home/ingredients_create/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('home/ingredients/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient_delete'),


    path('home/dishtype/', DishTypeListView.as_view(), name='dishtype'),
    path('home/dishtype_create/', DishTypeCreateView.as_view(), name='dishtype_create'),
    path('home/dishtype/delete/<int:pk>/', DishTypeDeleteView.as_view(), name='dishtype_delete'),

]
