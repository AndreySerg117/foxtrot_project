from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField("Ім'я", max_length=12, blank=False, null=False)
    last_name = models.CharField("Призвіще", max_length=24, blank=False, null=False)
    patronymic = models.CharField("По батькові", max_length=36, blank=False, null=False)
    document_in_passport = models.CharField("Документ пасспорта", max_length=24, blank=False, null=False)
    nn_in_passport = models.CharField("nn пасспорта", max_length=24, blank=False, null=False)
    photo = models.ImageField("Фото", null=True, blank=True, upload_to="user_photos/")
