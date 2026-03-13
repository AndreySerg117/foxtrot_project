from django.shortcuts import render, redirect
from apps.users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import logging


@login_required(login_url='/users/login')
def index(request):
    return render(request, "index.html", context={"data": 123})


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
