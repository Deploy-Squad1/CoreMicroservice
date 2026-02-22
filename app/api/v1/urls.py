from django.urls import path

from .views import LoginView, LogoutView, RefreshTokenView, UserView

urlpatterns = [
    path("users/", UserView.as_view(), name="users"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
