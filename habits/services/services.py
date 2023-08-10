import pytz
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from config.settings import TIME_ZONE
from random import sample
from user_auth.models import User
from habits.models import Habits, BotMessages
from config.settings import BOT_URL, bot_token


class Bot_message():

    def __init__(self) -> None:
        self.token = bot_token
        self.url_bot = BOT_URL

    def get_url(self, *args, **kwargs) -> str:
        method = kwargs.get('method')
        self.url = f'{self.url_bot}{self.token}/{method}'
        return self.url

    @staticmethod
    def generate_new_password() -> str:
        password = "".join(sample("".join([str(i) for i in range(
            0, 10)]) + "*+-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 10))
        return password

    def get_last_message_id(self) -> int:
        # Находим самое последнее сообщение
        last_message_id = BotMessages.objects.all().order_by("-id").first()
        if last_message_id:
            return last_message_id.message_id
        return 0

    def get_user_or_create(chat_id, first_name):
        if User.objects.filter(chat_id=chat_id).exists():
            # Пользователь уже есть в базе.
            user = User.objects.get(chat_id=chat_id)
        else:
            # Создаем нового пользователя
            password = self.generate_new_password()
            user = User.objects.create(
                chat_id=chat_id,
                first_name=first_name,
                is_staff=False,
                is_superuser=False
            )
            user.set_password(password)
            user.save()
        return user

    def send_list_or_gen_password(self, chat_id, first_name):
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
        last_message_id = self.get_last_message_id()
        url = self.get_url(method='getUpdates')
        response = requests.get(
            url,
        ).json()
        if response['ok'] == True:
            result = response['result']
            for update in result:
                # print("update=", update)
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
            print(response)

            # print("message=", message)
            # print("chat_id=", chat_id)
            # print("text=", text)

    def send_message(self, *args, **kwargs):
        url = self.get_url(method='sendMessage')
        chat_id = kwargs.get('chat_id')
        text = kwargs.get('text')
        response = requests.get(url, params={'chat_id': chat_id, 'text': text})


    @staticmethod
    def is_now_time_for_send(habit):
        # current_tz_name = timezone.get_current_timezone_name()
        # current_tz = pytz.timezone(TIME_ZONE)
        # timezone.activate(current_tz)
        datetime_now = timezone.now()
        # datetime_now = datetime_now.astimezone(timezone.utc).replace(tzinfo=None)
        # print("datetime_now =", datetime_now)
        # print("current_tz=", current_tz)
        # print(habit.time)
        # print(habit.last_time_send)
        # print(habit.period)
        # print(habit.datetime_start)
        # if habit.datetime_start is None:
        #     datetime_naive = timezone.make_naive(datetime_now, timezone.get_current_timezone())
        #     print("datetime_naive=", datetime_naive)

        #     # naive = datetime_now()
        #     # print("naive=", naive)
        #     # naive.replace(tzinfo=zoneinfo.ZoneInfo("Europe/Helsinki"))

        #     habit.datetime_start = datetime_naive
        #     habit.save()
        if habit.period == 'every 15 minutes':
            next = timedelta(minutes=15)
        elif habit.period == 'hourly':
            next = timedelta(hours=1)
        elif habit.period == 'daily':
            next = timedelta(days=1)
        else:
            next = timedelta(days=7)
        print("next=", next)
        if habit.last_time_send:
            next_time = habit.last_time_send + next
            if next_time >= datetime_now:
                # print("Пора")
                # print("next_time=", next_time, " datetime_now=", datetime_now)
                # print("habit=" , habit)
                return True
            else:
                # print("Еще не время")
                # print("next_time=", next_time, " datetime_now=", datetime_now)
                # print("habit=" , habit)
                return False
        else:
            return True

    def send_habits(self):
        # скрипт для рассылки напоминаний
        habits = Habits.objects.filter(user__is_subscripted=True)
        print(habits)
        for habit in habits:
            if self.is_now_time_for_send(habit):
                chat_id = habit.user
                text = "Время выполнить привычку: " + str(habit)
                if not habit.is_pleasant:
                    if habit.compensation:
                        text += "\nВознаграждение за выполнение: " + habit.compensation
                    else:
                        text += "\nВознаграждение за выполнение: " + habit.linked_habit
                self.send_message(chat_id=habit.user, text=text)
                habit.last_send = timezone.now()
                habit.save()


def send_message_bot():
    bot = Bot_message()
    bot.get_updates()
    bot.send_habits()