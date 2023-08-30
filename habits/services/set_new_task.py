import json
import datetime
import pytz
from celery.schedules import crontab, timedelta
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule
from habits.models import Habits
from config.settings import TIME_ZONE
from config.settings import BASE_DIR
import os
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
        task = create_periodic_task(habit)

