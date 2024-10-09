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

# Home page view with statistics
def home(request):
    context = {
        'cooks_count': Chef.objects.count(),  # Total number of chefs
        'dishes_count': Recipe.objects.count(),  # Total number of dishes
        'dish_types_count': dishType.objects.count(),  # Total number of dish types
        'ingredients': Ingredient.objects.count(),  # Total number of ingredients
    }
    return render(request, 'home.html', context)

# Login page
def login(request):
    # If the user is already authenticated, redirect to the home page
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home page

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# View and add ingredients
def ingredients(request):
    search_form = IngredientNameSearchForm(request.GET)  # Search form for filtering ingredients
    if search_form.is_valid() and search_form.cleaned_data['name']:
        ingredients = Ingredient.objects.filter(name__icontains=search_form.cleaned_data['name'])
    else:
        ingredients = Ingredient.objects.all()

    # Form for adding a new ingredient
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredients')  # Redirect to ingredient list after successful addition
    else:
        form = IngredientForm()

    return render(request, 'ingredients.html', {
        'ingredients': ingredients,
        'form': form,
        'search_form': search_form
    })

# Create a new ingredient
def ingredient_create(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredients')  # Redirect to ingredient list after addition
    else:
        form = IngredientForm()

    return render(request, 'ingredients_create.html', {'form': form})

# Create a new dish/recipe
def dishes_create(request):
    # Process the form for adding a new recipe
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dishes')  # Redirect to the dish list after saving
    else:
        form = RecipeForm()

    return render(request, 'dishes_create.html', {'form': form})

# View and search dishes
def dishes(request):
    search_form = RecipeNameSearchForm(request.GET)  # Search form for filtering recipes
    if search_form.is_valid() and search_form.cleaned_data['name']:
        recipes = Recipe.objects.filter(name__icontains=search_form.cleaned_data['name'])
    else:
        recipes = Recipe.objects.all()

    return render(request, 'dishes_list.html', {
        'recipes': recipes,
        'search_form': search_form
    })

# View and search cooks/chefs
def cooks(request):
    search_form = ChefUsernameSearchForm(request.GET)  # Search form for filtering chefs
    if search_form.is_valid() and search_form.cleaned_data['username']:
        chefs = Chef.objects.filter(username__icontains=search_form.cleaned_data['username'])
    else:
        chefs = Chef.objects.all()

    return render(request, 'cooks_list.html', {
        'chefs': chefs,
        'search_form': search_form
    })

# Create a new cook/chef
def cooks_create(request):
    if request.method == 'POST':
        form = ChefCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Chef created successfully!")  # Success message
            return redirect('cooks')  # Redirect to the cook list after saving
    else:
        form = ChefCreationForm()

    return render(request, 'cooks_create.html', {
        'form': form
    })

# View dish types
def dishtypes(request):
    search_form = dishTypeNameSearchForm(request.GET)  # Search form for filtering dish types
    if search_form.is_valid() and search_form.cleaned_data['name']:
        dishtypes = dishType.objects.filter(name__icontains=search_form.cleaned_data['name'])
    else:
        dishtypes = dishType.objects.all()

    return render(request, 'dishtype_list.html', {
        'dishtypes': dishtypes,
        'search_form': search_form
    })

# Create a new dish type
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

# Delete a chef
@login_required
def chef_delete(request, pk):
    chef = get_object_or_404(Chef, pk=pk)  # Get the specific chef by ID
    chef.delete()
    return redirect('cooks')

# Delete an ingredient
@login_required
def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)  # Get the specific ingredient by ID
    ingredient.delete()
    return redirect('ingredients')

# Delete a recipe
@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)  # Get the specific recipe by ID
    recipe.delete()
    return redirect('dishes')

# Delete a dish type
@login_required
def dishtype_delete(request, pk):
    dishtype = get_object_or_404(dishType, pk=pk)  # Get the specific dish type by ID
    dishtype.delete()
    return redirect('dishtype')
