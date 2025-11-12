from django.urls import path
from core import views
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy

app_name = "core"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
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
    # reset password urls
    path(
        "password_reset/",
        PasswordResetView.as_view(success_url=reverse_lazy("core:password_reset_done")),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("core:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
