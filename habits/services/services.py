import requests
from random import sample
from user_auth.models import User
from habits.models import Habits
from config.settings import BOT_URL, bot_token

class Bot_message():

    def __init__(self):
        self.token = bot_token
        self.url_bot = BOT_URL

    def get_url(self, *args, **kwargs):
        method = kwargs.get('method')
        self.url = f'{self.url_bot}{self.token}/{method}'
        return self.url

    @staticmethod
    def generate_new_password():
        password = "".join(sample("".join([str(i) for i in range(0,10)]) + "*+-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 10))
        return password


    def get_updates(self, *args, **kwargs):
        url = self.get_url(method='getUpdates')
        response = requests.get(
            url,
            # data=data
        ).json()
        if response['ok'] == True:
            result = response['result']
            for update in result:
                message = update['message']
                text = message['text']
                chat_id = message['chat']['id']
                first_name = message['chat']['first_name']
                if User.objects.filter(chat_id=chat_id).exists():
                    user = User.objects.filter(chat_id=chat_id)[0]
                    message = "Список ваших привычек:\n"
                    habits = Habits.objects.filter(user=user)
                    for habit in habits:
                        message += str(habit) + "\n"
                    self.send_message(
                        chat_id=chat_id,
                        text=message
                        )
                else:
                    password = self.generate_new_password()
                    new_user = User.objects.create(
                        chat_id=chat_id,
                        first_name=first_name,
                        is_staff=False,
                        is_superuser=False
                    )
                    new_user.set_password(password)
                    new_user.save()
                    self.send_message(
                        chat_id=chat_id,
                        text=f"Вам установлен пароль для доступа к сайту:\n{password}"
                        )
                # print("message=", message)
                # print("chat_id=", chat_id)
                # print("text=", text)


    def send_message(self, *args, **kwargs):
        url = self.get_url(method='sendMessage')
        chat_id = kwargs.get('chat_id')
        text = kwargs.get('text')
        # print("text=", text)
        # print("chat_id=", chat_id)
        response = requests.get(url, params={'chat_id': chat_id, 'text': text})
        # print(response.status_code)
        # print(response.json())
        return response.json()
