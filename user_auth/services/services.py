from user_auth.models import User
import datetime

import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule


def something():
    print("test")
# def set_schedule(*args, **kwargs):

#     schedule, created = IntervalSchedule.objects.get_or_create(
#          every=10,
#          period=IntervalSchedule.SECONDS,
#      )

#     PeriodicTask.objects.create(
#          interval=schedule,
#          name='Importing contacts',
#          task='user_auth.tasks.task_check_last_login',
#          args=json.dumps(['arg1', 'arg2']),
#          kwargs=json.dumps({
#             'be_careful': True,
#          }),
#          expires=datetime.utcnow() + timedelta(seconds=30)
#      )
