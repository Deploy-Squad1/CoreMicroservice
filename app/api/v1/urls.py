from django.urls import path

from .views import LoginView, UserView

urlpatterns = [
    path("users/", UserView.as_view(), name="users"),
    path("login/", LoginView.as_view(), name="login"),
]
