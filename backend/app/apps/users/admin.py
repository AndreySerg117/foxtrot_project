from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from apps.users.models import Shop

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


class SellerInline(admin.TabularInline):
    model = User
    fk_name = "shop"
    extra = 1
    fields = ("username", "last_name", "patronymic")
    verbose_name = "Продавець"
    verbose_name_plural = "Продавці"


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user_count")
    search_fields = ("title",)
    inlines = [SellerInline]

    def user_count(self, obj):
        return obj.sellers.count()

    user_count.short_description = "Кількість продавців"


