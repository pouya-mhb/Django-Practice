from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from .models import UserProfile


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    avatar = profile.avatar
    return render(
        request,
        "dashboard.html",
        {
            "posts": user_posts,
            "comments": user_comments,
            "avatar": avatar,
        },
    )


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
                return redirect("dashboard")
            else:
                return HttpResponse("Account disabled")
        else:
            messages.warning(request, "Invalid Login")
            return redirect("core:login")

    else:
        form = LoginForm()
        return render(request, "core/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return render(request, "core/logout.html")
