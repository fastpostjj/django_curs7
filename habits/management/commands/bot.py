import requests
from django.core.management import BaseCommand
from config.settings import BOT_URL, bot_token
from habits.services.services import Bot_message


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = Bot_message()
        bot.get_updates()
        bot.send_habits()




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
