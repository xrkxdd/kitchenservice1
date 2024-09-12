from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RecipeForm, IngredientForm
from .models import dishType, Chef, Recipe, Ingredient


@admin.register(Chef)
class ChefAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "years_of_experience",
                    "contract_size",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "years_of_experience",
                    "contract_size",
                )
            },
        ),
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    search_fields = ("name",)
    list_filter = ("chefs",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    form = IngredientForm
    search_fields = ("name",)
    list_filter = ("recipes",)


admin.site.register(dishType)
