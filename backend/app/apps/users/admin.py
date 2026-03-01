from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "first_name", "last_name",
                    "patronymic", "document_in_passport", "nn_in_passport", "photo_preview")
    search_fields = ("first_name", "last_name", "patronymic")
    fieldsets = (
        ("Additional info", {"fields": ("patronymic", "document_in_passport",
                                        "nn_in_passport", "photo", "photo_preview")}),
    ) + UserAdmin.fieldsets
    readonly_fields = ("photo_preview",)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="100" style="object-fit: cover; border-radius: 5px;" />',
                obj.photo.url,
            )
        return "-"

    photo_preview.short_description = "Photo Preview"

