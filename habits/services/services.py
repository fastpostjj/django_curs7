from habits.services.bot_message import Bot_message
import json
import pytz
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule
from config.settings import TIME_ZONE, CELERY_BEAT_SCHEDULE


def check_message_bot():
    # проверяем новые сообщения и добавляем новых пользователей
    bot = Bot_message()
    return bot.get_updates()


def create_schedule(period='hourly'):
    """
    функция создает расписание для периодических задач
    """
    if period == 'every 15 minutes':
        return IntervalSchedule.objects.get_or_create(
            every=15,
            period=IntervalSchedule.MINUTES,
        )
    elif period == 'hourly':
        return IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
    elif period == 'daily':
        return IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )
    elif period == 'weekly':
        return IntervalSchedule.objects.get_or_create(
            every=7,
            period=IntervalSchedule.DAYS,
        )
    else:
        return IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )


def del_periodic_task(habit):
    """
    функция удаления периодической задачи рассылки привычки
    """
    name = habit.get_name_periodic_task()
    task_habit = PeriodicTask.objects.filter(name=name)
    # Если задача с таким именем существует - удаляем ее
    if task_habit:
        task_habit.delete()
        if name in CELERY_BEAT_SCHEDULE:
            CELERY_BEAT_SCHEDULE.pop([name], None)


def create_periodic_task(habit):
    """
    функция создания периодической задачи рассылки привычки
    """
    period = habit.period
    chat_id = habit.user.chat_id
    text = "Время выполнить привычку: " + str(habit)
    if not habit.is_pleasant:
        if habit.compensation:
            text += "\nВознаграждение за выполнение: " + \
                str(habit.compensation)
        else:
            text += "\nВознаграждение за выполнение: " + \
                str(habit.linked_habit)
    # Создаем интервал для повтора
    schedule, created = create_schedule(period)
    name = habit.get_name_periodic_task()
    task_habit = PeriodicTask.objects.filter(name=name)
    start_time = timezone.datetime.combine(
        timezone.now().today(),
        habit.time)

    start_time = timezone.make_aware(
        start_time,
        timezone=pytz.timezone(TIME_ZONE)
    )

    if not task_habit.exists():
        # Создаем задачу для повторения
        task_habit = PeriodicTask.objects.create(
            interval=schedule,
            name=name,
            start_time=start_time,
            task='habits.tasks.send_one_message_bot',
            kwargs=json.dumps({
                'chat_id': chat_id,
                'text': text
            }),
        )
        CELERY_BEAT_SCHEDULE[name] = {
                'task': 'habits.tasks.send_one_message_bot',  # Путь к задаче
                'schedule': schedule,  # Расписание выполнения задачи
                'kwargs': json.dumps(
                    {
                        'chat_id': chat_id,
                        'text': text
                    }
                    )
            }
    return task_habit


def update_periodic_task(old_habit, habit):
    """
    функция обновления периодической задачи рассылки привычки
    """
    # удаляем старую задачу по рассылке
    del_periodic_task(old_habit)
    # и создаем новую
    return create_periodic_task(habit)
