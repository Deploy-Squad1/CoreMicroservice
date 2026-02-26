from django.conf import settings
from django.shortcuts import redirect

from app.models import IPBlocklist
from app.services import IPBlocklistService


# pylint: disable=R0903
class CheckBlockedIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META["REMOTE_ADDR"]
        ip_hash = IPBlocklistService.hash(ip_address)

        if IPBlocklist.objects.filter(ip_address=ip_hash).exists():
            return redirect(settings.BLOCKED_IP_REDIRECT_URL)

        response = self.get_response(request)
        return response
