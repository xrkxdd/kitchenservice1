from django.test import TestCase
from django.urls import reverse
from kitchen.models import DishType, Chef, Ingredient, Recipe
from django.test import TestCase

class DishTypeModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Salad")

    def test_str_method(self):
        self.assertEqual(str(self.dish_type), "Salad")


class ChefModelTest(TestCase):
    def setUp(self):
        self.chef = Chef.objects.create_user(username="chef1", password="chefpassword", first_name="John", last_name="Doe")

    def test_str_method(self):
        self.assertEqual(str(self.chef), "chef1 (John Doe)")


class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Tomato", source="Local Farm", unit="kg", price=2.50)

    def test_str_method(self):
        self.assertEqual(str(self.ingredient), "Tomato (Local Farm - kg at 2.50)")


class RecipeModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Salad")
        self.recipe = Recipe.objects.create(name="Greek Salad", description="Healthy salad", price=10.00, kitchen_type=self.dish_type)

    def test_str_method(self):
        self.assertEqual(str(self.recipe), "Greek Salad")

    def test_total_cost(self):
        ingredient1 = Ingredient.objects.create(name="Feta", source="Greek Farm", unit="kg", price=4.00)
        ingredient2 = Ingredient.objects.create(name="Olives", source="Local Farm", unit="kg", price=3.00)
        self.recipe.ingredients.add(ingredient1, ingredient2)
        self.assertEqual(self.recipe.total_cost, 7.00)




from kitchen.forms import RecipeForm, ChefCreationForm, IngredientForm

class RecipeFormTest(TestCase):
    def test_form_valid(self):
        ingredient = Ingredient.objects.create(name="Tomato", source="Local", unit="kg", price=3.00)
        dish_type = DishType.objects.create(name="Salad")
        chef = Chef.objects.create_user(username="chef", password="pass")

        form_data = {
            'name': 'New Recipe',
            'description': 'Tasty dish',
            'price': 15.00,
            'kitchen_type': dish_type.pk,
            'chefs': [chef.pk],
            'ingredients': [ingredient.pk],
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_ingredients(self):
        dish_type = DishType.objects.create(name="Salad")
        form_data = {
            'name': 'Recipe Without Ingredients',
            'description': 'Tasty dish',
            'price': 15.00,
            'kitchen_type': dish_type.pk,
            'chefs': [],
            'ingredients': [],
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['ingredients'])


class ChefCreationFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            'username': 'newchef',
            'password1': 'mypassword123',
            'password2': 'mypassword123',
            'years_of_experience': 5,
            'first_name': 'John',
            'last_name': 'Doe',
            'contract_size': 160,
        }
        form = ChefCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'username': 'newchef',
            'password1': 'mypassword123',
            'password2': 'mismatchpassword',
            'years_of_experience': -1,
        }
        form = ChefCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Years of experience should be greater than zero.', form.errors['years_of_experience'])


class IngredientFormTest(TestCase):
    def test_form_valid(self):
        form_data = {'name': 'Salt', 'source': 'Sea', 'unit': 'kg', 'price': 1.00}
        form = IngredientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {'name': '', 'source': 'Sea', 'unit': 'kg', 'price': -1.00}
        form = IngredientForm(data=form_data)
        self.assertFalse(form.is_valid())


class UrlTests(TestCase):
    def test_home_url(self):
        response = self.client.get(reverse('kitchen:home'))
        self.assertEqual(response.status_code, 200)

    def test_chef_list_url(self):
        response = self.client.get(reverse('kitchen:cooks'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_url(self):
        response = self.client.get(reverse('kitchen:dishes'))
        self.assertEqual(response.status_code, 200)

    def test_dish_type_create_url(self):
        response = self.client.get(reverse('kitchen:dishtype_create'))
        self.assertEqual(response.status_code, 200)
