from django.core.management.base import BaseCommand, CommandError

from tours.models import DefaultTour


class Command(BaseCommand):
    args = ''
    help = 'Creates default default tours.'

    def handle(self, *args, **options):
        DefaultTour.objects.all().delete()

        times_of_day = (
            (10, 45),
            (11, 45),
            (12, 45),
        )

        days_of_week = range(6)

        for day_num in days_of_week:
            for hour, minute in times_of_day:
                DefaultTour.objects.create(
                    source='Information Office',
                    minute=minute,
                    hour=hour,
                    day_num=day_num,
                    length=75,
                )
