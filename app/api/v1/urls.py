from django.urls import path

from .views import (
    HealthCheckView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    RegistrationView,
    InviteEmailView,
)

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("health/", HealthCheckView.as_view(), name="health"),
    path("invite/email/", InviteEmailView.as_view(), name="invite-email")
]
