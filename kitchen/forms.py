from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import dishType

from kitchen.models import Recipe, Chef, Ingredient


class RecipeForm(forms.ModelForm):
    # Field for selecting multiple chefs using checkboxes
    chefs = forms.ModelMultipleChoiceField(
        queryset=Chef.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    # Field for selecting multiple ingredients using checkboxes (required)
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Recipe
        fields = "__all__"  # Use all fields from the Recipe model

    # Custom validation for ingredients field
    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients')
        if not ingredients:
            raise ValidationError("At least one ingredient is required.")
        return ingredients


class ChefCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Chef
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
            "contract_size",
        )  # Add custom fields to the standard user creation form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help text for password fields
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        # Remove password-based authentication field if it exists
        if 'password_based_authentication' in self.fields:
            del self.fields['password_based_authentication']


class ChefExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = ["years_of_experience", "contract_size"]

    # Custom validation for years of experience field
    def clean_years_of_experience(self) -> int:
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])

    # Optionally, you could add validation for contract_size if needed
    # def clean_contract_size(self):
    #     contract_size = self.cleaned_data.get('contract_size')
    #     # Add custom validation logic here
    #     return contract_size


# Validation function for years of experience
def validate_years_of_experience(years_of_experience: str) -> int:
    try:
        years_of_experience = int(years_of_experience)
        if years_of_experience <= 0:
            raise ValidationError("Years of experience should be greater than zero.")
    except ValueError:
        raise ValidationError("Years of experience should be a valid positive integer.")

    return years_of_experience


class ChefUsernameSearchForm(forms.Form):
    # Search form for filtering chefs by username
    username = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by username",
            "class": "form-control",  # Optionally, add class for styling
            "maxlength": "150",
        }),
    )


class RecipeNameSearchForm(forms.Form):
    # Search form for filtering recipes by name
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class dishTypeNameSearchForm(forms.Form):
    # Search form for filtering dish types by name
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class IngredientForm(forms.ModelForm):
    # Field for selecting multiple recipes using checkboxes
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Ingredient
        fields = "__all__"  # Use all fields from the Ingredient model


class IngredientNameSearchForm(forms.Form):
    # Search form for filtering ingredients by name
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class dishTypeForm(forms.ModelForm):
    class Meta:
        model = dishType
        fields = ['name']  # Only include the 'name' field of the dishType model
