# myapp/management/commands/what_time_is_it.py

from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'Displays the current date and time'

    def handle(self, *args, **kwargs):
        current_time = timezone.now()
        self.stdout.write(self.style.SUCCESS(f"The current time is: {current_time}"))
