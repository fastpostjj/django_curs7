from django.core.management import BaseCommand
from habits.services.set_tasks import set_tasks


class Command(BaseCommand):
    def handle(self, *args, **options):
        set_tasks()
