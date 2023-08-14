import requests
from django.core.management import BaseCommand
from config.settings import BOT_URL, bot_token
from habits.services.services import Bot_message
# import redis

import json
from datetime import datetime, timedelta
from habits.services.set_new_task import create_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        создаем задачи по отправке привычек по расписанию
        """
        # bot = Bot_message()
        # bot.get_updates()
        create_task()
