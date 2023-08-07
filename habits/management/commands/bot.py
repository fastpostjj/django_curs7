from django.core.management import BaseCommand
from config.settings import BOT_URL, bot_token
import requests


# from habits.services.services import print_url

class Command(BaseCommand):
    def get_url(self, *args, **kwargs):
        method = kwargs.get('method')
        url = f'{BOT_URL}{bot_token}/{method}'
        print(url)
        return url

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
                chat_id = message['chat']['id']

                text = message['text']
                # print("message=", message)
                print("chat_id=", chat_id)
                print("text=", text)

    def send_message(self, *args, **kwargs):
        url = self.get_url(method='sendMessage')
        chat_id = kwargs.get('chat_id')
        text = kwargs.get('text')
        print("text=", text)
        print("chat_id=", chat_id)
        response = requests.get(url, params={'chat_id': chat_id, 'text': text})
        print(response.status_code)
        print(response.json())
        return response.json()



    def handle(self, *args, **options):
        method = 'getMe'
        # self.get_updates()
        # self.send_message(chat_id=729962006, text="тестовое сообщение")



#         Чтобы использовать этот режим, передайте MarkdownV2 в поле parse_mode. Используйте в сообщении следующий синтаксис:

# *bold \*text*
# _italic \*text_
# __underline__
# ~strikethrough~
# ||spoiler||
# *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
# [inline URL](http://www.example.com/)
# [inline mention of a user](tg://user?id=123456789)
# ![👍](tg://emoji?id=5368324170671202286)
# `inline fixed-width code`
# ```
# pre-formatted fixed-width code block
# ```
# ```python
# pre-formatted fixed-width code block written in the Python programming language
# ```
