# from datetime import datetime, timedelta
# from django.utils import timezone
from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule


def set_tasks():
    """"
    функция создает периодическую задачу:
    -   habits.tasks.check_message - задача проверки новых
    сообщений от телеграм-бота каждую минуту
    """

    time_check_messages = 1
    # Проверяем, есть ли уже такой интервал, если нет -создаем его
    schedule_check = IntervalSchedule.objects.filter(
        every=time_check_messages,
        period=IntervalSchedule.MINUTES
    )
    if not schedule_check.exists():
        schedule_check = IntervalSchedule.objects.create(
            every=time_check_messages,
            period=IntervalSchedule.MINUTES
        )
    else:
        schedule_check = schedule_check.first()

    task_check = PeriodicTask.objects.filter(
        name='Check_message',
        task='habits.tasks.check_message'
    )

    # Проверяем есть ли такая задача и если нет - создаем задачу
    # для проверки новых сообщений
    if not task_check.exists():
        PeriodicTask.objects.create(
            interval=schedule_check,
            name='Check_message',
            task='habits.tasks.check_message'
        )


def set_task_send_habits():
    """
    -   habits.tasks.send_habits - задача рассылки привычек
    по расписанию каждые 5 минут
    !!!Не используется

    """
    time_send_habits = 5

    # Создаем интервал для повтора
    schedule_send = IntervalSchedule.objects.filter(
        every=time_send_habits,
        period=IntervalSchedule.MINUTES
    )
    if not schedule_send.exists():
        schedule_send = IntervalSchedule.objects.create(
            every=time_send_habits,
            period=IntervalSchedule.MINUTES
        )
    else:
        schedule_send = schedule_send.first()

    task_send = PeriodicTask.objects.filter(
        name='Send_habit',
        task='habits.tasks.send_habits'
    )

    # Создаем задачу рассылки привычек
    if not task_send.exists():
        PeriodicTask.objects.create(
            interval=schedule_send,
            name='Send_habit',
            task='habits.tasks.send_habits'
        )
