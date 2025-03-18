from django.urls import path
from .views import activate,register_user
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)



urlpatterns = [
    path("register/",register_user,name="register"),
    path("activate/<str:uidb64>/<str:token>/",activate,name="activate"),
    path(
        "login/",
        LoginView.as_view(template_name="authentication/login.html"),
        name="login",
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(template_name="authentication/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(template_name="authentication/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="authentication/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]