import json
from django_celery_beat.models import PeriodicTask
from habits.models import Habits
from habits.services.services import create_periodic_task, create_schedule
from config.settings import CELERY_BEAT_SCHEDULE


def create_task_sending_habits():
    """"
    функция создания периодических задач по рассылке привычек по расписанию
    """
    # Отбираем привычки только для подписанных пользователей
    habits = Habits.objects.filter(user__is_subscripted=True)
    for habit in habits:
        # Если нет такой задачи - создаем
        try:
            name = habit.get_name_periodic_task()
            task = PeriodicTask.objects.get(name=name)
            schedule = create_schedule(habit)

            # добавляем в расписание
            if name not in CELERY_BEAT_SCHEDULE:
                CELERY_BEAT_SCHEDULE[name] = {
                    'task': 'habits.tasks.send_one_message_bot',  # Путь к задаче
                    'schedule': schedule,  # Расписание выполнения задачи
                    'kwargs': json.dumps(
                        {
                            'chat_id': habit.user.chat_id,
                            'text': json.loads(task.kwargs).get('text')
                        }
                        )
                }
        except PeriodicTask.DoesNotExist:
            create_periodic_task(habit)
    # print("CELERY_BEAT_SCHEDULE=", CELERY_BEAT_SCHEDULE)
    return habits
