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
        # period = habit.period
        # chat_id = habit.user.chat_id
        # text = "Время выполнить привычку: " + str(habit)
        # if not habit.is_pleasant:
        #     if habit.compensation:
        #         text += "\nВознаграждение за выполнение: " + \
        #             str(habit.compensation)
        #     else:
        #         text += "\nВознаграждение за выполнение: " + \
        #             str(habit.linked_habit)

        # # Создаем интервал для повтора
        # schedule, created = create_schedule(period)
        # name = habit.get_name_periodic_task()
        # task_habit = PeriodicTask.objects.filter(name=name)
        # start_time = timezone.datetime.combine(
        #     timezone.now().today(),
        #     habit.time)

        # start_time = timezone.make_aware(
        #     start_time,
        #     timezone=pytz.timezone(TIME_ZONE)
        # )

        # if not task_habit.exists():

        #     # Создаем задачу для повторения
        #     t = PeriodicTask.objects.create(
        #         interval=schedule,
        #         name=name,
        #         start_time=start_time,
        #         task='habits.tasks.send_one_message_bot',
        #         kwargs=json.dumps({
        #             'chat_id': chat_id,
        #             'text': text
        #         }),
        #     )
            # t = create_periodic_task(habit)
            # file_name = str(BASE_DIR) + os.sep + "log.txt"
            # with open(file_name, "a", encoding="utf-8") as file:
            #     file.write(f"create message {t}, start_time={t.start_time}")
