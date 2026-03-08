from django.urls import path

from app.api.internal.v1.views import AssignNewInquisitorView, PasscodeRotateView

urlpatterns = [
    path("passcode/rotate", PasscodeRotateView.as_view(), name="rotate-passcode"),
    path(
        "inquisitor/assign-new",
        AssignNewInquisitorView.as_view(),
        name="assign-new-inquisitor",
    ),
]
