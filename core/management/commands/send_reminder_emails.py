from django.core.management.base import BaseCommand
from core.tasks import send_reminder_emails


class Command(BaseCommand):
    args = ''
    help = "Sends reminder emails for tomorrow's tours and shifts."

    def handle(self, *args, **options):
        send_reminder_emails()
