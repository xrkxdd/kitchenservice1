from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import kitchen.views


from django.shortcuts import render
from .models import Chef, Recipe, dishType, Ingredient

def home(request):
    context = {
        'cooks_count': Chef.objects.count(),
        'dishes_count': Recipe.objects.count(),
        'dish_types_count': dishType.objects.count(),
        'ingredients': Ingredient.objects.count(),
    }
    return render(request, 'home.html', context)


def login(request):
    # Если пользователь уже аутентифицирован, перенаправляем на главную страницу
    if request.user.is_authenticated:
        return redirect('home')  # Перенаправление на главную страницу

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после логина
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

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

    return render(request, 'dishes_list.html', {
        'recipes': recipes,
        'form': form,
        'search_form': search_form
    })


# Просмотр списка поваров
def cooks(request):
    # Обработка формы для поиска
    search_form = ChefUsernameSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['username']:
        chefs = Chef.objects.filter(username__icontains=search_form.cleaned_data['username'])
    else:
        chefs = Chef.objects.all()

    return render(request, 'cooks_list.html', {
        'chefs': chefs,
        'search_form': search_form
    })

# Создание нового повара
def cooks_create(request):
    if request.method == 'POST':
        form = ChefCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cooks_create')
    else:
        form = ChefCreationForm()

    return render(request, 'cooks_create.html', {
        'form': form
    })


