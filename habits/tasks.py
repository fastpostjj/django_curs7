from habits.services.services import check_message_bot
from config.celery import app
from config.settings import BASE_DIR
from django.utils import timezone
import os
import json
from habits.services.services import Bot_message
from habits.services.set_new_task import create_task_sending_habits


@app.task
def check_message(*args):
    """
    периодическая задача вызывает функцию проверки
    новых сообщений от бота
    """
    check_message_bot()
    file_name = str(BASE_DIR) + os.sep + "log.txt"

    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"{timezone.now()} check_message_bot\n")


@app.task
def send_habits(*args):
    """
    периодическая задача вызывает функцию
    создания периодических задач
    рассылки привычек по расписанию
    """
    create_task_sending_habits()
    file_name = str(BASE_DIR) + os.sep + "log.txt"

    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"{timezone.now()} send_habits\n")


@app.task
def send_one_message_bot(*args, **kwargs):
    """
    отправка сообщения text пользователю chat_id в телеграм
    """
    bot = Bot_message()
    status = bot.send_message(*args, **kwargs)

    file_name = str(BASE_DIR) + os.sep + "log.txt"

    with open(file_name, "a") as file:
        file.write(f"{timezone.now()} send_one_message_bot kwargs= {kwargs}\n")
    return status
