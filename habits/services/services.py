from habits.services.bot_message import Bot_message


def check_message_bot():
    # проверяем новые сообщения и добавляем новых пользователей
    bot = Bot_message()
    return bot.get_updates()
