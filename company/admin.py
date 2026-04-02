from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "username", "email", "full_name", "is_staff", "is_active")
    search_fields = ("username", "email", "full_name", "phone")
    list_filter = ("is_staff", "is_superuser", "is_active")
    ordering = ("id",)

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "full_name",
                    "phone",
                    "address",
                    "city",
                    "state",
                    "country",
                    "postal_code",
                )
            },
        ),
    )

