from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class dishType(models.Model):
    name = models.CharField(max_length=255, unique=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("kitchen:dish-type-detail", kwargs={"pk": self.pk})


class Chef(AbstractUser):
    years_of_experience = models.IntegerField(null=True)
    contract_size = models.IntegerField(default=160)

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
        verbose_name = "chef"
        verbose_name_plural = "chefs"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self) -> str:
        return reverse("kitchen:chef-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    unit = models.CharField(max_length=10)
    purchase_price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"

    def __str__(self):
        return f"{self.name} ({self.provider} {self.unit} {self.purchase_price})"


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    kitchen_type = models.ForeignKey(
        dishType, on_delete=models.CASCADE, related_name="recipes"
    )
    chefs = models.ManyToManyField(Chef, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")

    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"

    def __str__(self):
        return self.name

    @property
    def total_cost(self) -> float:
        queryset = self.ingredients.all().aggregate(
            total_cost=models.Sum("purchase_price")
        )
        total_cost = queryset["total_cost"]
        return round(total_cost, 2) if total_cost is not None else 0.0

    @property
    def margin(self) -> float:
        if self.total_cost > 0:
            markup = ((self.price - self.total_cost) / self.total_cost) * 100
            return round(markup, 0)
        return 0
