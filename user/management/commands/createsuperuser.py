# users/management/commands/createsuperuser.py

from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = "Create a superuser with telegram_id"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--telegram_id",
            type=int,
            help="Telegram ID for the superuser",
        )

    def handle(self, *args, **options):
        telegram_id = options.get("telegram_id")

        if not telegram_id:
            telegram_id = self._get_telegram_id_interactively()

        options["telegram_id"] = telegram_id

        super().handle(*args, **options)

    def _get_telegram_id_interactively(self):
        while True:
            telegram_id = input("Telegram ID: ").strip()

            if not telegram_id.isdigit():
                self.stderr.write("Telegram ID must be a number.")
                continue

            return int(telegram_id)
