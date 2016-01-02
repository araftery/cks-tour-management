from django.core.management.base import BaseCommand
from core.tasks import send_reminder_texts


class Command(BaseCommand):
    args = ''
    help = "Sends reminder texts for today's tours and shifts."

    def handle(self, *args, **options):
        send_reminder_texts()
