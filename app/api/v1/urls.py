from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    RefreshTokenView,
    RegistrationView,
    VerifyPasscodeView,
)

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("passcode/verify/", VerifyPasscodeView.as_view(), name="check-passcode"),
]
