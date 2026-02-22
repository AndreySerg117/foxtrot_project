from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "first_name", "last_name",
                    "patronymic", "document_in_passport", "nn_in_passport", "is_active", "is_staff")
    search_fields = ("first_name", "last_name", "patronymic")
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("patronymic", "document_in_passport", "nn_in_passport")}),
    )

