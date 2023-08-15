import json
from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule
from habits.models import Habits


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


def create_task():
    """"
    функция создания периодических задач по рассылке привычек по расписанию
    """
    # Удаляем все задачи, в названии которых есть 'Habit ' и создаем новые
    task_habit = PeriodicTask.objects.filter(name__contains='Habit ')
    task_habit.delete()

    # Определяем временные интервалы для каждой периодичности
    habits = Habits.objects.filter(user__is_subscripted=True)
    for habit in habits:
        period = habit.period
        chat_id = habit.user
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

        name = "Habit " + str(habit.id) + " " + str(period)
        task_habit = PeriodicTask.objects.filter(name=name)
        if not task_habit.exists():

            # Создаем задачу для повторения
            PeriodicTask.objects.create(
                interval=schedule,
                name=name,
                # start_time=datetime.combine(timezone.now().today(),
                # habit.time),
                # start_time=timezone.now(),
                # start_time=timezone.localtime(),
                task='habits.tasks.send_one_message_bot',
                # args=json.dumps(['arg1', 'arg2']),
                kwargs=json.dumps({
                    'chat_id': chat_id,
                    'text': text
                }),
                # expires=datetime.utcnow() + timedelta(seconds=30)
            )
