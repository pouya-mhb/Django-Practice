from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    return render(request, "home.html")


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful")
            return redirect("core:login")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Login successful")
                return redirect("home")
            else:
                return HttpResponse("Account disabled")
        else:
            return HttpResponse("Invalid login")
    else:
        form = LoginForm()
        return render(request, "core/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return render(request, "core/logout.html")
