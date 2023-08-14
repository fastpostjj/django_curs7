from asyncio import sleep
import pytz
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task
from config.settings import TIME_ZONE
from random import sample
from user_auth.models import User
from habits.models import Habits, BotMessages
from config.settings import BOT_URL, bot_token
import json


class Bot_message():
    """
    класс Bot_message для отправки и получения сообщений телеграм-бота
    """

    def __init__(self) -> None:
        """
        инициализация объекта бота
        """
        self.token = bot_token
        self.url_bot = BOT_URL

    def get_url(self, *args, **kwargs) -> str:
        """
        возвращает url для api бота
        """
        method = kwargs.get('method')
        self.url = f'{self.url_bot}{self.token}/{method}'
        return self.url

    @staticmethod
    def generate_new_password() -> str:
        """
        генерирует новый пароль
        """
        password = "".join(sample("".join([str(i) for i in range(
            0, 10)]) + "*+-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 10))
        return password

    def get_last_message_id(self) -> int:
        """
        Находит самое последнее сохраненное сообщение в базе для дальнейшей
        проверки новых сообщений
        """
        last_message_id = BotMessages.objects.all().order_by("-id").first()
        if last_message_id:
            return last_message_id.message_id
        return 0

    def send_list_or_gen_password(self, chat_id, first_name):
        """
        в ответ на новое сообщение отправляет:
         - новому пользователю генерирует пароль и добавляет в  данных
         - существующему пользователю список его привычек
        """
        if User.objects.filter(chat_id=chat_id).exists():
            # Пользователь уже есть в базе.
            # Отправляем ему список его привычек
            user = User.objects.get(chat_id=chat_id)
            message = "Список ваших привычек:\n"
            habits = Habits.objects.filter(user=user)
            for habit in habits:
                message += str(habit) + "\n"
            self.send_message(
                chat_id=chat_id,
                text=message
            )
        else:
            # Новому пользователю генерируем пароль
            # для доступа и заносим его в базу
            password = self.generate_new_password()
            user = User.objects.create(
                chat_id=chat_id,
                first_name=first_name,
                email='test@test.ru',
                is_staff=False,
                is_superuser=False
            )
            user.set_password(password)
            user.save()
            self.send_message(
                chat_id=chat_id,
                text=f"Ваш id {chat_id} добавлен в базу.\n"
                + f" Вам установлен пароль для доступа к сайту:\n{password}.\n"
                + f" Вы можете настроить список привычек для рассылки напоминаний.\n"
                + f" Для начала отправки необходимо установить пользователю статус is_subscripted=True.\n"
            )
        return user

    def get_updates(self, *args, **kwargs):
        """
        проверка новых сообщений в чате
        """
        last_message_id = self.get_last_message_id()
        url = self.get_url(method='getUpdates')
        response = requests.get(
            url,
        ).json()
        if response['ok'] == True:
            result = response['result']
            for update in result:
                message = update['message']
                message_id = message['message_id']
                text = message['text']
                chat_id = message['chat']['id']
                first_name = message['chat']['first_name']
                if message_id > last_message_id:
                    # Нового пользователя добавляем в базу, существующему
                    # отправляем список его привычек
                    user = self.send_list_or_gen_password(chat_id, first_name)
                    # Новое сообщение сохраняем в базу
                    new_message = BotMessages.objects.create(
                        message_id=message_id,
                        message_text=text,
                        user=user
                    )
                    new_message.save()
        else:
            print("Ответ не подлежит обработке: ", response)
            return False

    def send_message(self, *args, **kwargs):
        """
        отправка сообщения пользователю телеграм
        """
        url = self.get_url(method='sendMessage')
        chat_id = kwargs.get('chat_id')
        text = kwargs.get('text')
        response = requests.get(url, params={'chat_id': chat_id, 'text': text})
        return response.status_code

    # @staticmethod
    # def is_now_time_for_send(habit):
    #     current_time = timezone.now()
    #     # Определяем временные интервалы для каждой периодичности
    #     intervals = {
    #         'every 15 minutes': timedelta(minutes=15),
    #         'hourly': timedelta(hours=1),
    #         'daily': timedelta(days=1),
    #         'weekly': timedelta(weeks=1)
    #     }

    #     datetime_now = timezone.now()

    #     next = intervals[habit.period]
    #     print("next=", next)
        # Проверяем, отправляли ли уже сообщение с данной привычкой в течение периода
        # if not habit.last_time_send:
        #     # ни разу не отправляли
        #     print("Время отправки привычки :", habit.time)
        # if BotMessages.objects.filter(
        #         user=habit.user,
        #         message_text=habit.activity,
        #         last_time_send=current_time-intervals[habit.period]).exists():
        #     print("Привычка для отправки: ", BotMessages.objects.filter(
        #         user=habit.user,
        #         message_text=habit.activity,
        #         last_time_send=current_time-intervals[habit.period]).exists())


        # if habit.last_time_send:
        #     next_time = habit.last_time_send + next
        #     print()
        #     if next_time >= current_time:
        #         print("Пора")
        #         print("next_time=", next_time, " current_time=", current_time)
        #         print("habit=", habit, " habit.period=", habit.period)
        #         return True
        #     else:
        #         print("Еще не время")
        #         print("next_time=", next_time, " current_time=", current_time)
        #         print("habit=", habit, " habit.period=", habit.period)
        #         return False
        # else:
        #     # еще ни разу не отправляли
        #     next_time = habit.time
        #     print("\nНи разу не отправляли")
        #     print("next_time=", next_time, " current_time=", current_time)
        #     print("habit=", habit, " habit.time=",
        #           habit.time, " habit.period=", habit.period)
        #     if habit.time == current_time:
        #         print("Пора")
        #         print("next_time=", next_time, " current_time=", current_time)
        #         print("habit=", habit, " habit.period=", habit.period)
        #         return True
        #     else:
        #         print("Еще не время")

        #     return False

    # @staticmethod
    # def get_next_time_for_send(habit:Habits) -> timedelta:
    #     print()
    #     print("habit=", habit)
    #     print("habit.last_time_send=", habit.last_time_send)
    #     print("habit.time=", habit.time)
    #     print("habit.period=", habit.period)
    #     current_time = timezone.now()
    #     # Определяем временные интервалы для каждой периодичности
    #     intervals = {
    #         'every 15 minutes': timedelta(minutes=15),
    #         'hourly': timedelta(hours=1),
    #         'daily': timedelta(days=1),
    #         'weekly': timedelta(weeks=1)
    #     }
    #     if habit.last_time_send:
    #         # Если уже отправляли
    #         print("intervals[habit.period]=", intervals[habit.period])
    #         next_time =  habit.last_time_send.time() + intervals[habit.period]
    #         while next_time < current_time:
    #             next_time +=  intervals[habit.period]
    #             print("next_time=, next_time")
    #     else:
    #         # если еще ни разу не отправляли
    #         next_time =  habit.time
    #         while next_time < current_time:
    #             next_time +=  intervals[habit.period]
    #             print("next_time=, next_time")
    #     return next_time

    # def send_habits(self):
    #     # скрипт для рассылки напоминаний

    #     # habits = Habits.objects.filter(
    #     # user__is_subscripted=True,
    #     # time=current_time
    #     # )
    #     current_time = timezone.now()
    #     stop_time = timezone.now() + timedelta(minutes=1)
    #     while current_time < stop_time:
    #         habits = Habits.objects.all()
    #         # print("Привычки для рассылки: ", habits)
    #         for habit in habits:
    #             print(" habit.time=", habit.time, " current_time=", current_time, " habit=", habit)
    #             print("Время следующей отправки ", self.get_next_time_for_send(habit))
    #             if habit.time == current_time:


    #             # if self.is_now_time_for_send(habit):
    #                 chat_id = habit.user
    #                 text = "Время выполнить привычку: " + str(habit)
    #                 if not habit.is_pleasant:
    #                     if habit.compensation:
    #                         text += "\nВознаграждение за выполнение: " + \
    #                             str(habit.compensation)
    #                     else:
    #                         text += "\nВознаграждение за выполнение: " + \
    #                             str(habit.linked_habit)
    #                 print(text)
    #             #     send_message_delay.delay(chat_id=habit.user, text=text, time=0)
    #                 send_message(chat_id=habit.user, text=text, time=0)
    #                 habit.last_send = timezone.now()
    #                 habit.save()
    #         current_time = timezone.now()

