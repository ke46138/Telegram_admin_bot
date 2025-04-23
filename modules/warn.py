from modules import sqlite_adapter as sq
from config import admins, allowed_chats

def setup_warn_handlers(bot):

    @bot.message_handler(commands=['unwarn'])
    def unwarn(message):
        """Регистрируем обработчик команды /unwarn"""
        print(52)
        if message.from_user:
            user_id = message.from_user.id
        elif message.sender_chat:
            user_id = message.sender_chat.id
        else:
            bot.reply_to(message, "Ошибка: не удалось определить отправителя.")
            return

        if user_id not in admins and user_id not in allowed_chats:
            bot.reply_to(message, "У вас нет прав на использование этой команды.")
            return

        try:
            if message.reply_to_message:
                sq.unwarn(message.reply_to_message.from_user.id, message.chat.id)
                bot.reply_to(message, "Варны удалены.")
            else:
                bot.reply_to(message, "Использование: /unwarn")
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {str(e)}")