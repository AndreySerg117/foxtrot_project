from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField("Ім'я", max_length=12, blank=False, null=False)
    last_name = models.CharField("Призвіще", max_length=24, blank=False, null=False)
    patronymic = models.CharField("По батькові", max_length=36, blank=False, null=False)
    document_in_passport = models.CharField("Документ пасспорта", max_length=24, blank=False, null=False)
    nn_in_passport = models.CharField("nn пасспорта", max_length=24, blank=False, null=False)
    photo = models.ImageField("Фото", null=True, blank=True, upload_to="user_photos/")
    shop = models.ForeignKey(
        "Shop",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sellers",
        verbose_name="Магазин"
    )


class Shop(models.Model):
    title = models.CharField(max_length=24)
    poster = models.ImageField(upload_to="albums/posters/%Y/%m/%d/", blank=False, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
