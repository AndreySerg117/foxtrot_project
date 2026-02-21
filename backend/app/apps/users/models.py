from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=12, blank=False, null=False)
    last_name = models.CharField(max_length=24, blank=False, null=False)
    patronymic = models.CharField(max_length=36, blank=False, null=False)
    document_in_passport = models.CharField(max_length=24, blank=False, null=False)
    nn_in_passport = models.CharField(max_length=24, blank=False, null=False)
