import requests
from django.conf import settings
from requests import HTTPError, RequestException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.services import PasscodeService


class PasscodeRotateView(APIView):
    def post(self, request):
        plain_passcode = PasscodeService.generate_plain()

        try:
            response = requests.post(
                settings.EMAIL_SERVICE_BASE_URL + "/send-daily-password",
                json={
                    "daily_password": plain_passcode,
                },
                timeout=600,
            )
        except RequestException as exc:
            return Response(
                exc.args[0].args, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            response.raise_for_status()
        except HTTPError as exc:
            return Response(exc.args, status=response.status_code)

        PasscodeService.update(plain_passcode)
        return Response(status=status.HTTP_200_OK)
