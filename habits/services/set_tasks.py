# from datetime import datetime, timedelta
# from django.utils import timezone
from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule


def set_tasks():
    """"
    функция создает 2 периодические задачи:
    -   habits.tasks.check_message - задача проверки новых
    сообщений от телеграм-бота каждые 5 минут
    -   habits.tasks.send_habits - задача рассылки привычек
    по расписанию каждые 3 минуты

    """
    # Проверяем, есть ли уже такой интервал, если нет -создаем его
    schedule_check = IntervalSchedule.objects.filter(
        every=5,
        period=IntervalSchedule.MINUTES
    )
    if not schedule_check.exists():
        schedule_check = IntervalSchedule.objects.create(
            every=5,
            period=IntervalSchedule.MINUTES
        )
    else:
        schedule_check = schedule_check.first()

    task_check = PeriodicTask.objects.filter(
        name='Check_message',
        task='habits.tasks.check_message'
    )

    # Проверяем есть ли такая задача и создаем если нет задачу
    # для проверки новых сообщений
    if not task_check.exists():
        PeriodicTask.objects.create(
            interval=schedule_check,
            # start_time=timezone.now(),
            name='Check_message',
            task='habits.tasks.check_message'
        )

    # Создаем интервал для повтора
    schedule_send = IntervalSchedule.objects.filter(
        every=3,
        period=IntervalSchedule.MINUTES
    )
    if not schedule_send.exists():
        schedule_send = IntervalSchedule.objects.create(
            every=3,
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
            # start_time=timezone.now(),
            task='habits.tasks.send_habits'
        )
