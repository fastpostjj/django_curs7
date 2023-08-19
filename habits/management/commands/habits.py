from django.core.management import BaseCommand
from habits.services.set_new_task import create_task_sending_habits


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        создаем задачи по отправке привычек по расписанию
        """
        create_task_sending_habits()
