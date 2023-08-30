import requests
from django.core.management import BaseCommand
from habits.services.set_tasks import set_tasks
# import redis


class Command(BaseCommand):
    """
    cсоздание периодической задачи проверки
      новых сообщений от бота
    """
    def handle(self, *args, **options):
        set_tasks()
