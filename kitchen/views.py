from django.shortcuts import render, redirect
from django.http import HttpResponse

import kitchen.views


def home(request):
    return render(request, 'home.html')


def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from .models import Ingredient, Recipe, Chef
from .forms import (
    IngredientForm, RecipeForm, ChefCreationForm, ChefExperienceUpdateForm,
    IngredientNameSearchForm, RecipeNameSearchForm, ChefUsernameSearchForm
)

# Ингредиенты: просмотр и добавление
def ingredients(request):
    # Обработка формы для поиска
    search_form = IngredientNameSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['name']:
        ingredients = Ingredient.objects.filter(name__icontains=search_form.cleaned_data['name'])
    else:
        ingredients = Ingredient.objects.all()

    # Обработка формы для добавления нового ингредиента
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredients')  # После успешного добавления
    else:
        form = IngredientForm()

    return render(request, 'ingredients.html', {
        'ingredients': ingredients,
        'form': form,
        'search_form': search_form
    })

# Блюда: просмотр и добавление
def dishes(request):
    # Обработка формы для поиска
    search_form = RecipeNameSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['name']:
        recipes = Recipe.objects.filter(name__icontains=search_form.cleaned_data['name'])
    else:
        recipes = Recipe.objects.all()

    # Обработка формы для добавления нового рецепта
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dishes')
    else:
        form = RecipeForm()

    return render(request, 'dishes.html', {
        'recipes': recipes,
        'form': form,
        'search_form': search_form
    })

# Повар: просмотр и добавление
def cooks(request):
    # Обработка формы для поиска
    search_form = ChefUsernameSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['username']:
        chefs = Chef.objects.filter(username__icontains=search_form.cleaned_data['username'])
    else:
        chefs = Chef.objects.all()

    # Обработка формы для добавления нового повара
    if request.method == 'POST':
        form = ChefCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cooks')
    else:
        form = ChefCreationForm()

    return render(request, 'cooks.html', {
        'chefs': chefs,
        'form': form,
        'search_form': search_form
    })

