from django.db import models
from config.settings import NULLABLE
from datetime import timedelta
from user_auth.models import User

# Create your models here.
"""
Модели
В книге хороший пример привычки описывается как конкретное действие, которое можно уложить в одно предложение:

я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

За каждую полезную привычку необходимо себя вознаграждать или сразу после делать приятную привычку. Но при этом привычка не должна расходовать на выполнение больше 2 минут. Исходя из этого получаем первую модель — Привычка.

Привычка:
Пользователь — создатель привычки.
Место — место, в котором необходимо выполнять привычку.
Время — время, когда необходимо выполнять привычку.
Действие — действие, которое представляет из себя привычка.
Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.
Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.
Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.
Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.
Обратите внимание, что в проекте у вас может быть больше, чем одна описанная здесь модель.

"""


class TelegramUser(models.Model):

    """
    chat_id
    phone
    is_subscripted
    """

    # username = None
    chat_id = models.IntegerField(
        verbose_name="chat_id",
        **NULLABLE)
    phone = models.CharField(
        max_length=35,
        verbose_name='телефон',
        **NULLABLE)
    is_subscripted = models.BooleanField(
        verbose_name="Подписан",
        default=False)

    # USERNAME_FIELD = 'chat_id'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return f"chat_id={self.chat_id}"

    class Meta:
        verbose_name = 'пользователь телеграма'
        verbose_name_plural = 'пользователи телеграма'


class Habits(models.Model):
    """
    Модель привычки-конкретное действие, которое можно уложить в одно предложение:

    я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

    Пользователь — создатель привычки.
    Место — место, в котором необходимо выполнять привычку.
    Время — время, когда необходимо выполнять привычку.
    Действие — действие, которое представляет из себя привычка.
    user
    place
    time
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
    is_pleasant = models.CharField(
        verbose_name='Приятная/полезная привычка',
        max_length=11,
        choices=[
            ('is_pleasant', 'приятная'),
            ('is_useful', 'полезная')
        ],
        default='is_useful'
    )
    is_public = models.BooleanField(
        verbose_name='Публичная',
        default=False
    )
    compensation = models.CharField(
        verbose_name="Вознаграждение за полезную привычку",
        max_length=200,
        **NULLABLE
    )
    linked_habit = models.ForeignKey(
        'self',
        verbose_name="Связанная приятная привычка",
        on_delete=models.SET_NULL,
        **NULLABLE
    )

    def __repr__(self) -> str:
        time = self.time.strftime('%H:%M')
        return f'я буду {self.activity} в {time} в {self.place}'

    def __str__(self) -> str:
        time = self.time.strftime('%H:%M')
        return f'я буду {self.activity} в {time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        unique_together = ('user', 'place', 'period', 'activity')
