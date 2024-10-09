from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class dishType(models.Model):
    # Model for representing a type of dish
    name = models.CharField(max_length=255, unique=False)  # Name of the dish type

    class Meta:
        ordering = ["name"]  # Default ordering by name

    def __str__(self):
        return self.name  # String representation of the dish type

    # Method to get the absolute URL for dishType detail view
    def get_absolute_url(self) -> str:
        return reverse("kitchen:dish-type-detail", kwargs={"pk": self.pk})


class Chef(AbstractUser):
    # Chef model extending the default Django user model
    years_of_experience = models.IntegerField(null=True)  # Number of years of experience
    contract_size = models.IntegerField(default=160)  # Default contract size (e.g., working hours)

    # Custom relationship with Django's Group and Permission models
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

    # Method to get the absolute URL for Chef detail view
    def get_absolute_url(self) -> str:
        return reverse("kitchen:chef-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    # Ingredient model representing food items used in recipes
    name = models.CharField(max_length=255)  # Name of the ingredient
    provider = models.CharField(max_length=255)  # Provider of the ingredient
    unit = models.CharField(max_length=10)  # Unit of measurement (e.g., kg, g)
    purchase_price = models.DecimalField(max_digits=7, decimal_places=2)  # Price per unit

    class Meta:
        verbose_name = "ingredient"  # Singular name for Ingredient in the admin interface
        verbose_name_plural = "ingredients"  # Plural name for Ingredient in the admin interface

    def __str__(self):
        # String representation showing name, provider, unit, and price
        return f"{self.name} ({self.provider} {self.unit} {self.purchase_price})"


class Recipe(models.Model):
    # Recipe model representing a culinary recipe
    name = models.CharField(max_length=255)  # Name of the recipe
    description = models.TextField(max_length=255)  # Description of the recipe
    price = models.DecimalField(max_digits=7, decimal_places=2)  # Selling price of the recipe
    kitchen_type = models.ForeignKey(
        dishType, on_delete=models.CASCADE, related_name="recipes"
    )  # Relation to dishType, with cascading delete
    chefs = models.ManyToManyField(Chef, related_name="recipes")  # Many-to-many relation with chefs
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")  # Many-to-many relation with ingredients

    class Meta:
        verbose_name = "recipe"  # Singular name for Recipe in the admin interface
        verbose_name_plural = "recipes"  # Plural name for Recipe in the admin interface

    def __str__(self):
        return self.name  # String representation of the recipe

    # Property to calculate the total cost of all ingredients in the recipe
    @property
    def total_cost(self) -> float:
        queryset = self.ingredients.all().aggregate(
            total_cost=models.Sum("purchase_price")
        )  # Sum of all ingredient prices
        total_cost = queryset["total_cost"]
        return round(total_cost, 2) if total_cost is not None else 0.0  # Return total cost or 0 if none

    # Property to calculate the profit margin of the recipe
    @property
    def margin(self) -> float:
        if self.total_cost > 0:
            markup = ((self.price - self.total_cost) / self.total_cost) * 100  # Calculate markup percentage
            return round(markup, 0)  # Return rounded markup
        return 0  # Return 0 if total cost is zero
