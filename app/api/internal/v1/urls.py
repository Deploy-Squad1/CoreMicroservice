from django.urls import path

from app.api.internal.v1.views import PasscodeRotateView

urlpatterns = [
    path("passcode/rotate", PasscodeRotateView.as_view(), name="rotate-passcode"),
]
