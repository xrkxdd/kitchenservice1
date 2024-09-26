
from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dishes/', views.dishes, name='dishes'),
    path('cooks/', views.cooks, name='cooks'),
    path('ingredients/', views.ingredients, name='ingredients'),

]

