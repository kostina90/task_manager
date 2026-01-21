from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest

from .forms import RegisterForm
from .models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return HttpResponseBadRequest("Username and password are required.")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return HttpResponseBadRequest("Invalid credentials.")

        login(request, user)
        return render(request, "user/login_success.html")

    return render(request, "user/login.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            user = authenticate(
                request,
                username=user.username,
                password=form.cleaned_data["password1"],
            )
            login(request, user)

            return render(request, "user/login_success.html")
    else:
        form = RegisterForm()

    return render(request, "user/register.html", {"form": form})
