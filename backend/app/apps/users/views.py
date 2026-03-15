from django.shortcuts import render, redirect
from apps.users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from apps.users.models import User, Shop
import logging
from django.views.generic import DetailView
from django.db.models import Q, prefetch_related_objects
from django.views.generic import DetailView
from django.contrib import messages


@login_required(login_url='/users/login')
def index(request):
    shops = Shop.objects.prefetch_related("sellers").all()
    q = request.GET.get('q', "").strip()
    if q:
        shops = shops.filter(
            Q(title__icontains=q)
            | Q(sellers__first_name__icontains=q)
            | Q(sellers__last_name__icontains=q)
            | Q(sellers__username__icontains=q)
        ).distinct()

        if shops:
            messages.success(request, f"Результати пошуку для запиту '{q}' ")
        else:
            messages.error(request, f"Нічого не знайдено для запиту '{q}' ")
    prefetch_related_objects(shops, "sellers")

    return render(request, "index.html", context={"shops": shops})


logger = logging.Logger(__name__)


def signup(request):
    logger.error(request.method)
    logger.error(request.user)
    logger.error(request.user.is_authenticated)
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('/')

    context = {"form": form, "form_title": "Sign up"}
    return render(request, 'signup.html', context)


def login_view(request):

    form = CustomAuthenticationForm(request)

    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('index')
    context = {"form": form, 'form_title': "Login"}
    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


class ShopDetailView(DetailView):
    model = Shop
    template_name = "shop_detail.html"
    context_object_name = 'shop'

    def get_queryset(self):
        return super().get_queryset().prefetch_related("sellers")

