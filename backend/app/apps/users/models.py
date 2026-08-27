from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=12, blank=False, null=False)
    last_name = models.CharField(max_length=24, blank=False, null=False)
    patronymic = models.CharField(max_length=36, blank=True, null=False)
    document_in_passport = models.CharField(max_length=24, blank=True, null=False)
    nn_in_passport = models.CharField(max_length=24, blank=True, null=False)
    photo = models.ImageField(null=True, blank=True, upload_to="user_photos/")
    shop = models.ForeignKey(
        "Shop",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sellers",
    )


class Shop(models.Model):
    title = models.CharField(max_length=256)
    poster = models.ImageField(upload_to="shops/", blank=False, null=True)
    description = models.TextField(blank=False, null=True)

    def __str__(self):
        return f"{self.title}"


class EmailVerificationCode(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE
        )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    last_sent_at = models.DateTimeField(default=timezone.now)
