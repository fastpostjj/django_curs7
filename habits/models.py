from django.db import models
from config.settings import NULLABLE
from datetime import timedelta
from user_auth.models import User

# Create your models here.
"""
Модели
В книге хороший пример привычки описывается как конкретное действие, которое
можно уложить в одно предложение:

я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

За каждую полезную привычку необходимо себя вознаграждать или сразу после
делать приятную привычку. Но при этом привычка не должна расходовать
на выполнение больше 2 минут. Исходя из этого получаем
первую модель — Привычка.

Привычка:
Пользователь — создатель привычки.
Место — место, в котором необходимо выполнять привычку.
Время — время, когда необходимо выполнять привычку.
Действие — действие, которое представляет из себя привычка.
Признак приятной привычки — привычка, которую можно привязать
к выполнению полезной привычки.
Связанная привычка — привычка, которая связана с другой привычкой,
важно указывать для полезных привычек, но не для приятных.
Периодичность (по умолчанию ежедневная) — периодичность выполнения
привычки для напоминания в днях.
Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
Время на выполнение — время, которое предположительно потратит
пользователь на выполнение привычки.
Признак публичности — привычки можно публиковать в общий доступ,
чтобы другие пользователи могли брать в пример чужие привычки.
Обратите внимание, что в проекте у вас может быть больше,
чем одна описанная здесь модель.

"""


class Habits_abstract(models.Model):
    """
    Абстрактный класс для описания модели привычки.
    Модель привычки-конкретное действие, которое можно уложить
    в одно предложение:

    я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

    Пользователь — создатель привычки.
    Место — место, в котором необходимо выполнять привычку.
    Время — время, когда необходимо выполнять привычку.
    Действие — действие, которое представляет из себя привычка.
    user
    place

    time

    datetime_start
    activity
    period
    is_pleasant
    is_useful
    is_public
    compensation

    """
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.SET_NULL,
        **NULLABLE
    )
    activity = models.CharField(
        verbose_name="Действие",
        max_length=200
    )
    time = models.TimeField(
        verbose_name="Время"
    )
    place = models.CharField(
        verbose_name="Место",
        max_length=150,
        **NULLABLE
    )
    period = models.CharField(
        verbose_name='Периодичность',
        max_length=16,
        choices=[
            ('every 15 minutes', 'каждые 15 минут'),
            ('hourly', 'ежечасно'),
            ('daily', 'ежедневно'),
            ('weekly', 'еженедельно')
        ],
        default='daily'
    )
    time_for_action = models.DurationField(
        verbose_name="Время на выполнение",
        default=timedelta(seconds=120)
    )
    is_pleasant = models.BooleanField(
        verbose_name="Приятная привычка",
        default=False
    )

    is_public = models.BooleanField(
        verbose_name='Публичная',
        default=False
    )

    def get_name_periodic_task(self):
        return f"Habit {self.id} {self.period}"

    def __repr__(self) -> str:
        time = self.time.strftime('%H:%M')
        return f'я буду {self.activity} в {time} в {self.place},'\
            + f' длительность :{self.time_for_action} ' + \
            f'{self.get_period_display()}'

    def __str__(self) -> str:
        time = self.time.strftime('%H:%M')
        return f'я буду {self.activity} в {time} в {self.place},'\
            + f' длительность :{self.time_for_action} ' + \
            f'{self.get_period_display()}'

    class Meta:
        abstract = True


class Habits(Habits_abstract):
    """
    Класс привычек.
    """
    compensation = models.CharField(
        verbose_name="Вознаграждение за полезную привычку",
        max_length=200,
        **NULLABLE
    )
    linked_habit = models.ForeignKey(
        'self',
        # related_name='pleasant_habit',
        verbose_name="Связанная приятная привычка",
        on_delete=models.SET_NULL,
        **NULLABLE
    )

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'


class BotMessages(models.Model):
    """
    Сообщения пользователей, полученные от бота
    message_id
    message_text
    user
    """
    message_id = models.IntegerField(
        verbose_name="id сообщения"
    )
    message_text = models.CharField(
        verbose_name="текст сообщения",
        max_length=300,
        **NULLABLE
    )
    user = models.ForeignKey(
        User,
        verbose_name="пользователь",
        on_delete=models.SET_NULL,
        **NULLABLE
    )

    def __str__(self):
        return f"id:{self.message_id} {self.message_text} {self.user}"

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
