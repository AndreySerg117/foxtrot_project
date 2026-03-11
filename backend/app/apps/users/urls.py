from django.urls import path
from apps.users.views import signup
from apps.users.views import index

urlpatterns = [
    path("", index),
    path("users/signup", signup, name='signup')
]
