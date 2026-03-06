from django.core.management.base import BaseCommand

from app.services import EmailService, PasscodeService


class Command(BaseCommand):
    help = "Rotate daily passcode and notify users"

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating new passcode...")

        plain_passcode = PasscodeService.generate_plain()
        PasscodeService.update(plain_passcode)

        self.stdout.write("Sending passcode email...")

        EmailService.send_passcode_email(
            to_email="user@example.com",
            passcode=plain_passcode,
        )

        self.stdout.write(self.style.SUCCESS("Passcode rotation completed"))
