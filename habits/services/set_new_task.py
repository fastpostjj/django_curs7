from django_celery_beat.models import PeriodicTask
from habits.models import Habits
from habits.services.services import create_periodic_task


def create_task_sending_habits():
    """"
    функция создания периодических задач по рассылке привычек по расписанию
    """
    # Удаляем все задачи, в названии которых есть 'Habit ' и создаем новые
    task_habit = PeriodicTask.objects.filter(name__contains='Habit ')
    task_habit.delete()

    # Определяем временные интервалы для каждой периодичности
    habits = Habits.objects.filter(user__is_subscripted=True)
    for habit in habits:
        create_periodic_task(habit)
