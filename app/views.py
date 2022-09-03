from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import LoginForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/dashboard")
                else:
                    form.invalid_login_error()
            else:
                form.invalid_login_error()
    else:
        form = LoginForm()

    return render(request, "app/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data

            username = data.get("username")
            password = data.get("password")

            authenticate(username=username, password=password)
            return redirect("/login")
        else:
            print(form.errors.as_data())
    else:
        form = UserCreationForm()

    return render(request, "app/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/login")


@login_required
def dashboard_view(request):
    return render(request, "app/dashboard.html")
