from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, ProfileEditForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from .models import UserProfile
from shop.models import Order, OrderItem


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by(
        "-created"
    )  # latest first
    user_posts = Post.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    avatar = profile.avatar
    return render(
        request,
        "dashboard.html",
        {
            "profile": profile,
            "posts": user_posts,
            "comments": user_comments,
            "avatar": avatar,
            "orders": orders,
        },
    )


@login_required
def edit_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, "core/edit_profile.html", {"form": form})


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            UserProfile.objects.create(user=user)

            messages.success(request, "Registration successful")
            return redirect("core:login")
        else:
            print(form.errors)
            messages.error(request, "Please correct the errors below.")
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
