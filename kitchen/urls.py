from django.urls import path
from . import views
from .views import dishes_create
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login, name='login'),  # Начальная страница login
    path('home/', views.home, name='home'),  # Главная страница
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # URL для выхода
    path('home/dishes/', views.dishes, name='dishes'),
    path('dishes/create/', dishes_create, name='dishes_create'),
    path('home/cooks/', views.cooks, name='cooks'),
    path('home/ingredients/', views.ingredients, name='ingredients'),  # Просмотр списка ингредиентов
    path('home/ingredients_create/', views.ingredient_create, name='ingredient_create'),  # Создание нового ингредиента
    path('home/cooks_create/', views.cooks_create, name='cooks_create'),
    path('home/dishtype/', views.dishtypes, name='dishtype'),
    path('home/dishtype_create/', views.dishtypes_create, name='dishtype_create'),
    path('home/cooks/delete/<int:pk>/', views.chef_delete, name='chef_delete'),
    path('home/ingredients/delete/<int:pk>/', views.ingredient_delete, name='ingredient_delete'),
    path('home/dishes/delete/<int:pk>/', views.recipe_delete, name='recipe_delete'),
    path('home/dishtype/delete/<int:pk>/', views.dishtype_delete, name='dishtype_delete'),
]
