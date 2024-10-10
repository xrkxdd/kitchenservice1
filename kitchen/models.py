from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from decimal import Decimal

class DishType(models.Model):
    """Model representing a type of dish."""
    name = models.CharField(max_length=255, unique=False)  # Name of the dish type

    class Meta:
        ordering = ["name"]  # Default ordering by name

    def __str__(self):
        return self.name  # String representation of the dish type

    def get_absolute_url(self) -> str:
        return reverse("kitchen:dish-type-detail", kwargs={"pk": self.pk})


class Chef(AbstractUser):
    """Chef model extending the default Django user model."""
    years_of_experience = models.IntegerField(null=True)  # Number of years of experience
    contract_size = models.IntegerField(default=160)  # Default contract size (e.g., working hours)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='chef_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='chef_permission_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = "chef"  # Singular name for Chef in the admin interface
        verbose_name_plural = "chefs"  # Plural name for Chef in the admin interface

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"  # String representation of the Chef

    def get_absolute_url(self) -> str:
        return reverse("kitchen:chef-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    """Ingredient model representing food items used in recipes."""
    name = models.CharField(max_length=255)  # Name of the ingredient
    source = models.CharField(max_length=255)  # Source/provider of the ingredient
    unit = models.CharField(max_length=10)  # Unit of measurement (e.g., kg, g)
    price = models.DecimalField(max_digits=7, decimal_places=2)  # Price per unit (renamed to 'price')

    class Meta:
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"

    def __str__(self):
        return f"{self.name} ({self.source} - {self.unit} at {self.price:.2f})"


class Recipe(models.Model):
    """Recipe model representing a culinary recipe."""
    name = models.CharField(max_length=255)  # Name of the recipe
    description = models.TextField(max_length=255)  # Description of the recipe
    price = models.DecimalField(max_digits=7, decimal_places=2)  # Selling price of the recipe
    kitchen_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="recipes"
    )  # Relation to DishType, with cascading delete
    chefs = models.ManyToManyField(Chef, related_name="recipes")  # Many-to-many relation with chefs
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")  # Many-to-many relation with ingredients

    @property
    def margin(self) -> float:
        """Calculate the profit margin based on total cost."""
        if self.total_cost > 0:
            markup = ((Decimal(self.price) - Decimal(self.total_cost)) / Decimal(
                self.total_cost)) * 100  # Ensure Decimal types
            return round(markup, 2)  # Return rounded markup
        return 0.0  # Return 0 if total cost is zero


    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"

    def __str__(self):
        return self.name  # String representation of the recipe

    @property
    def total_cost(self) -> float:
        """Calculate total cost of all ingredients."""
        queryset = self.ingredients.all().aggregate(
            total_cost=models.Sum("price")  # Summing prices of all ingredients
        )
        total_cost = queryset["total_cost"]
        return round(total_cost, 2) if total_cost is not None else 0.0  # Return total cost or 0 if None

    @property
    def margin(self) -> float:
        """Calculate the profit margin based on total cost."""
        if self.total_cost > 0:
            markup = ((self.price - self.total_cost) / self.total_cost) * 100  # Calculate margin percentage
            return round(markup, 2)  # Return rounded markup
        return 0.0  # Return 0 if total cost is zero
