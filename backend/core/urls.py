from django.urls import path
from core import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy

app_name = "core"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    # change password urls
    path(
        "password_change/",
        PasswordChangeView.as_view(
            success_url=reverse_lazy("core:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
