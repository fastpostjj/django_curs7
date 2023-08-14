from habits.services.services import check_message_bot
from config.celery import app
from celery import shared_task
from config.settings import BASE_DIR
import os
from habits.services.services import Bot_message
from habits.services.set_new_task import create_task


@app.task
# @shared_task
def check_message(*args):
    """
    периодическая задача вызывает функцию проверки
    новых сообщений от бота
    """
    check_message_bot()
    file_name = str(BASE_DIR) + os.sep + "log.txt"

    with open(file_name, "a") as file:
        file.write("send_message_bot\n")


@app.task
def send_habits(*args):
    """
    периодическая задача вызывает функцию
    рассылки привычек по расписанию
    """
    create_task()
    file_name = str(BASE_DIR) + os.sep + "log.txt"

    with open(file_name, "a") as file:
        file.write("send_habits\n")


@app.task
def send_one_message_bot(*args, **kwargs):
    """
    отправка сообщения text пользователю chat_id в телеграм
    """
    chat_id = kwargs.get('chat_id')
    text = kwargs.get('text')
    bot = Bot_message()
    status = bot.send_message(chat_id, text)

    file_name = str(BASE_DIR) + os.sep + "log.txt"

    with open(file_name, "a") as file:
        file.write(f"send_one_message_bot {chat_id} {text} \n")
    return status
