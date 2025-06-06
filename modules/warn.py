from modules import sqlite_adapter as sq
#from config import admins, allowed_chats
from modules import auth
from modules import botdebug as d
from modules import mute
import traceback

def setup_warn_handlers(bot):

    @bot.message_handler(commands=['unwarn'])
    def unwarn(message):
        try:
            result = auth.authorize(message)

            if result == 0:
                bot.reply_to(message, "У вас нет прав на использование этой команды")
                return
            elif result == -1:
                bot.reply_to(message, "Ошибка: не удалось определить отправителя. ПОЗДРАВЛЯЮ, КАК ТЫ ЭТО СДЕЛАЛ?")
                return
            elif result == 1:
                pass
            else:
                raise ValueError("Итак вопрос: математика сломалась?")

            if message.reply_to_message:
                sq.unwarn(message.reply_to_message.from_user.id, message.chat.id)
                bot.reply_to(message, "Варны удалены.")
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которому хотите дать варн")
                return
        except:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(commands=['warn'])
    def warn(message):
        try:
            result = auth.authorize(message)

            if result == 0:
                bot.reply_to(message, "У вас нет прав на использование этой команды")
                return
            elif result == -1:
                bot.reply_to(message, "Ошибка: не удалось определить отправителя. ПОЗДРАВЛЯЮ, КАК ТЫ ЭТО СДЕЛАЛ?")
                return
            elif result == 1:
                pass
            else:
                raise ValueError("Итак вопрос: математика сломалась?")

            if message.reply_to_message:
                username = message.reply_to_message.from_user.username

                if username == None or username == "":
                    username = "USERNOTHAVEUSERNAME"

                args = message.text.split(' ')[1:]
                reason = ' '.join(args[1:]) if len(args) > 1 else "Причина не указана"

                result = sq.add_warn(message.reply_to_message.user.id, username, message.chat.id, reason)

                if result >= 15:
                    mute.mute(message.reply_to_message.user.id, message.chat.id, "Превышение кол-ва варнов", username, "1w")
                    sq.mute_user(message.reply_to_message.user.id, username, 604800, message.chat.id, "Превышение кол-ва варнов")
                else:
                    bot.reply_to(message, f"Добавлен варн. Текущее количество: {result}")
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которому хотите дать варн")
                return
        except:
            d.send_view_traceback(message, traceback.format_exc())
