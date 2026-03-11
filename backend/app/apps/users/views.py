from django.shortcuts import render, redirect
from apps.users.forms import CustomUserCreationForm
from django.contrib.auth import login
import logging


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

    context = {"form": form}
    return render(request, 'signup.html', context)
