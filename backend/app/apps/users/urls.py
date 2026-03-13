from django.urls import path
from apps.users.views import signup, login_view, logout_view
from apps.users.views import index

urlpatterns = [
    path("", index, name='index'),
    path("users/signup/", signup, name='signup'),
    path('users/login/', login_view, name='login'),
    path('users/logout/', logout_view, name='logout'),
]
