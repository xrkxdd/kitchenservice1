from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import dishType, Ingredient, Recipe, Chef
from .forms import (
    dishTypeForm, dishTypeNameSearchForm, IngredientForm, RecipeForm, ChefCreationForm,
    ChefExperienceUpdateForm, IngredientNameSearchForm, RecipeNameSearchForm, ChefUsernameSearchForm
)


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


# Просмотр и добавление ингредиентов
def ingredients(request):
    search_form = IngredientNameSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['name']:
        ingredients = Ingredient.objects.filter(name__icontains=search_form.cleaned_data['name'])
    else:
        ingredients = Ingredient.objects.all()

    # Форма добавления нового ингредиента
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredients')  # После успешного добавления перенаправление на список
    else:
        form = IngredientForm()

    return render(request, 'ingredients.html', {
        'ingredients': ingredients,
        'form': form,
        'search_form': search_form
    })

# Создание нового ингредиента
def ingredient_create(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredients')  # После добавления возвращаемся на список ингредиентов
    else:
        form = IngredientForm()

    return render(request, 'ingredients_create.html', {'form': form})


# Блюда: добавление нового рецепта
def dishes_create(request):
    # Обработка формы для добавления нового рецепта
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dishes')  # Перенаправляем на список рецептов после успешного сохранения
    else:
        form = RecipeForm()

    return render(request, 'dishes_create.html', {'form': form})

# Блюда: просмотр и поиск
def dishes(request):
    # Обработка формы для поиска
    search_form = RecipeNameSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['name']:
        recipes = Recipe.objects.filter(name__icontains=search_form.cleaned_data['name'])
    else:
        recipes = Recipe.objects.all()

    return render(request, 'dishes_list.html', {
        'recipes': recipes,
        'search_form': search_form
    })


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
            messages.success(request, "Chef created successfully!")  # Уведомление об успехе
            return redirect('cooks')  # Перенаправление на страницу со списком поваров
    else:
        form = ChefCreationForm()

    return render(request, 'cooks_create.html', {
        'form': form
    })


# Просмотр типов блюд
def dishtypes(request):
    # Форма поиска
    search_form = dishTypeNameSearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['name']:
        dishtypes = dishType.objects.filter(name__icontains=search_form.cleaned_data['name'])
    else:
        dishtypes = dishType.objects.all()

    return render(request, 'dishtype_list.html', {
        'dishtypes': dishtypes,
        'search_form': search_form
    })

# Создание нового типа блюда
def dishtypes_create(request):
    if request.method == 'POST':
        form = dishTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dishtype')
    else:
        form = dishTypeForm()

    return render(request, 'dishtype_create.html', {
        'form': form
    })



# Удаление повара
@login_required
def chef_delete(request, pk):
    chef = get_object_or_404(Chef, pk=pk)
    chef.delete()
    return redirect('cooks')

# Удаление ингредиента
@login_required
def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    ingredient.delete()
    return redirect('ingredients')

# Удаление рецепта
@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('dishes')

# Удаление типа блюда
@login_required
def dishtype_delete(request, pk):
    dishtype = get_object_or_404(dishType, pk=pk)
    dishtype.delete()
    return redirect('dishtype')
