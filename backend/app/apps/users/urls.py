from django.urls import path
from apps.users.views import (signup, login_view, logout_view, index, ShopDetailView, crud_users,
                              user_create, user_edit, user_delete)

urlpatterns = [
    path("", index, name='index'),
    path("users/signup/", signup, name='signup'),
    path('users/login/', login_view, name='login'),
    path('users/logout/', logout_view, name='logout'),
    path("shop/<int:pk>/", ShopDetailView.as_view(), name='shop_detail'),
    path('users/', crud_users, name='crud_users'),
    path('user/create', user_create, name='user_create'),
    path('user/edit/<int:pk>/', user_edit, name='user_edit'),
    path('user/delete/<int:pk>/', user_delete, name='user_delete')
]
