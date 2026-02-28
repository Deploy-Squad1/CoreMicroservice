from django.urls import path

from .views import (
    DropDatabaseDataView,
    HealthCheckView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    RegistrationView,
)

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("health/", HealthCheckView.as_view(), name="health"),
    path("database/delete/", DropDatabaseDataView.as_view(), name="drop-database"),
]
