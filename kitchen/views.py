from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import DishType, Ingredient, Recipe, Chef
from .forms import (
    DishTypeForm, DishTypeNameSearchForm, IngredientForm, RecipeForm, ChefCreationForm,
    IngredientNameSearchForm, RecipeNameSearchForm, ChefUsernameSearchForm
)

# Home page view with statistics
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cooks_count'] = Chef.objects.count()
        context['dishes_count'] = Recipe.objects.count()
        context['dish_types_count'] = DishType.objects.count()
        context['ingredients'] = Ingredient.objects.count()
        return context

# Login page
class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

# View and add ingredients
class IngredientListView(CreateView, ListView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients.html'
    context_object_name = 'ingredients'

    def get_queryset(self):
        search_form = IngredientNameSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data['name']:
            return Ingredient.objects.filter(name__icontains=search_form.cleaned_data['name'])
        return Ingredient.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = IngredientNameSearchForm(self.request.GET)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Ingredient added successfully!")
        return super().form_valid(form)

    # Define where to redirect after a successful form submission
    success_url = reverse_lazy('kitchen:ingredients')

# Create a new ingredient
class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients_create.html'

    def form_valid(self, form):
        messages.success(self.request, "Ingredient created successfully!")
        return super().form_valid(form)

    success_url = reverse_lazy('kitchen:ingredients')

# Create a new dish/recipe
class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'dishes_create.html'

    def form_valid(self, form):
        messages.success(self.request, "Recipe created successfully!")
        return super().form_valid(form)

    success_url = reverse_lazy('kitchen:dishes')

# View and search dishes
class RecipeListView(ListView):
    model = Recipe
    template_name = 'dishes_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        search_form = RecipeNameSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data['name']:
            return Recipe.objects.filter(name__icontains=search_form.cleaned_data['name'])
        return Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = RecipeNameSearchForm(self.request.GET)
        return context

# View and search cooks/chefs
class ChefListView(ListView):
    model = Chef
    template_name = 'cooks_list.html'
    context_object_name = 'chefs'

    def get_queryset(self):
        search_form = ChefUsernameSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data['username']:
            return Chef.objects.filter(username__icontains=search_form.cleaned_data['username'])
        return Chef.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ChefUsernameSearchForm(self.request.GET)
        return context

# Create a new cook/chef
class ChefCreateView(CreateView):
    model = Chef
    form_class = ChefCreationForm
    template_name = 'cooks_create.html'

    def form_valid(self, form):
        messages.success(self.request, "Chef created successfully!")
        return super().form_valid(form)

    success_url = reverse_lazy('kitchen:cooks')

# View dish types
class DishTypeListView(ListView):
    model = DishType
    template_name = 'dishtype_list.html'
    context_object_name = 'dishtypes'

    def get_queryset(self):
        search_form = DishTypeNameSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data['name']:
            return DishType.objects.filter(name__icontains=search_form.cleaned_data['name'])
        return DishType.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DishTypeNameSearchForm(self.request.GET)
        return context

# Create a new dish type
class DishTypeCreateView(CreateView):
    model = DishType
    form_class = DishTypeForm
    template_name = 'dishtype_create.html'

    def form_valid(self, form):
        messages.success(self.request, "Dish type created successfully!")
        return super().form_valid(form)

    success_url = reverse_lazy('kitchen:dishtype')

# Delete a chef
class ChefDeleteView(LoginRequiredMixin, DeleteView):
    model = Chef
    success_url = reverse_lazy('kitchen:cooks')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Chef deleted successfully!")
        return super().delete(request, *args, **kwargs)

# Delete an ingredient
class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = reverse_lazy('kitchen:ingredients')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Ingredient deleted successfully!")
        return super().delete(request, *args, **kwargs)

# Delete a recipe
class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('kitchen:dishes')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Recipe deleted successfully!")
        return super().delete(request, *args, **kwargs)

# Delete a dish type
class DishTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = DishType
    success_url = reverse_lazy('kitchen:dishtype')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Dish type deleted successfully!")
        return super().delete(request, *args, **kwargs)
