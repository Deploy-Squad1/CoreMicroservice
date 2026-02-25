from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.services import PasscodeService


class PasscodeRotateView(APIView):
    def post(self, request):
        plain_passcode = PasscodeService.generate_plain()

        # Send plain passcode to the email service
        # Throw exception if the service is unavailable
        # ...

        PasscodeService.update(plain_passcode)
        return Response(status=status.HTTP_200_OK)
