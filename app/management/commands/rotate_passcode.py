from django.core.management.base import BaseCommand

from app.services import PasscodeService


class Command(BaseCommand):
    help = "Rotate daily passcode"

    def add_arguments(self, parser):
        parser.add_argument("passcode", type=str)

    def handle(self, *args, **options):
        self.stdout.write("Generating new passcode...")

        plain_passcode = options["passcode"]
        PasscodeService.update(plain_passcode)

        self.stdout.write(self.style.SUCCESS("Passcode rotation completed"))
