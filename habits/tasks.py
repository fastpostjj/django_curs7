from celery import shared_task
from habits.services.services import send_message_bot
from config.settings import BASE_DIR
import os


@shared_task
def check_message_bot(*args):
    send_message_bot()
    file_name = str(BASE_DIR) + os.sep + "log.txt"
   
    with open(file_name, "a") as file:
        file.write("send_message_bot\n")
