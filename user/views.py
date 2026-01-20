from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponseBadRequest

from .forms import RegisterForm
from .models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        telegram_id = request.POST.get("telegram_id")

        if not username or not telegram_id:
            return HttpResponseBadRequest("Username and Telegram ID are required.")

        try:
            user = User.objects.get(username=username, telegram_id=telegram_id)
        except User.DoesNotExist:
            return HttpResponseBadRequest("Invalid credentials.")

        login(request, user)
        return render(request, "user/login_success.html")

    return render(request, "user/login.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "user/login_success.html")
    else:
        form = RegisterForm()

    return render(request, "user/register.html", {"form": form})
