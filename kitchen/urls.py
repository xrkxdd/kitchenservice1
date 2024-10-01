from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login, name='login'),  # Начальная страница login
    path('home/', views.home, name='home'),  # Главная страница
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # URL для выхода
    path('home/dishes/', views.dishes, name='dishes'),
    path('home/cooks/', views.cooks, name='cooks'),
    path('home/ingredients/', views.ingredients, name='ingredients'),
    path('home/cooks_create/', views.cooks_create, name='cooks_create'),
]

