from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),
]
