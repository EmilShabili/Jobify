from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = (
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_superuser"
    )
    list_filter = ("is_active", "is_superuser")
    fieldsets = (
        (
            "User information",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password"
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            "Create new user",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    readonly_fields = ("timestamp",)
    search_fields = ("email", "first_name","last_name",)
    ordering = ("email", "first_name","last_name",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)