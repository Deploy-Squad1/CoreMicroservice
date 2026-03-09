from django.urls import path

from .views import (
    AddIPToBlocklistView,
    CheckIPView,
    DropDatabaseDataView,
    HealthCheckView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    RegistrationView,
    UsersView,
    VerifyPasscodeView,
)

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("health/", HealthCheckView.as_view(), name="health"),
    path("users/", UsersView.as_view(), name="users"),
    path("ip/block/", AddIPToBlocklistView.as_view(), name="block-ip"),
    path("ip/check/", CheckIPView.as_view(), name="check-ip"),
    path("passcode/verify/", VerifyPasscodeView.as_view(), name="check-passcode"),
    path("database/delete/", DropDatabaseDataView.as_view(), name="drop-database"),
]
