from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import (signup, login_view, logout_view, index, ShopDetailView, crud_users,
                              user_create, user_edit, user_delete, user_redirect, crud_shops, shop_create,
                              shop_edit, shop_delete)

urlpatterns = [
    path("", index, name='index'),
    path("users/signup/", signup, name='signup'),
    path('users/login/', login_view, name='login'),
    path('users/logout/', logout_view, name='logout'),
    path("shop/<int:pk>/", ShopDetailView.as_view(), name='shop_detail'),
    path('users/', crud_users, name='crud_users'),
    path('user/create', user_create, name='user_create'),
    path('user/edit/<int:pk>/', user_edit, name='user_edit'),
    path('user/delete/<int:pk>/', user_delete, name='user_delete'),
    path('user/redirect/', user_redirect, name='user_redirect'),
    path('shops/', crud_shops, name='crud_shops'),
    path('shop/create', shop_create, name='shop_create'),
    path('shops/edit/<int:pk>/', shop_edit, name='shop_edit'),
    path('shop/delete/<int:pk>/', shop_delete, name='shop_delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
