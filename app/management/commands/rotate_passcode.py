from django.core.management.base import BaseCommand

from app.services import PasscodeService


class Command(BaseCommand):
    help = "Rotate daily passcode"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating new passcode...")

        plain_passcode = PasscodeService.generate_plain()

        PasscodeService.update(plain_passcode)

        self.stdout.write(self.style.SUCCESS("Passcode rotation completed"))
