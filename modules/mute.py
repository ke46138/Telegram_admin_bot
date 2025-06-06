from datetime import timedelta
from modules import auth
from modules import sqlite_adapter as sq
from modules import botdebug as d
import traceback

bot_g = ""

def setup_mute_handlers(bot):
    """Регистрируем обработчик команды /mute"""
    
    bot_g = bot

    @bot.message_handler(commands=['mute'])
    def mute(message):
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

            args = message.text.split(' ')[1:]
            if len(args) < 1:
                bot.reply_to(message, "Использование: /mute <время> <причина>")
                return

            time_arg = args[0]
            reason = ' '.join(args[1:]) if len(args) > 1 else "Причина не указана"

            # Парсим время (например, 10m или 2h)
            time_value = int(time_arg[:-1])
            time_unit = time_arg[-1]

            # Преобразуем время в секунды
            if time_unit == 'm':  # минуты
                mute_time = timedelta(minutes=time_value).total_seconds()
            elif time_unit == 'h':  # часы
                mute_time = timedelta(hours=time_value).total_seconds()
            elif time_unit == 'd': # дни
                mute_time = timedelta(days=time_value).total_seconds()
            elif time_unit == 'w': # недели
                mute_time = timedelta(weeks=time_value).total_seconds()
            else:
                bot.reply_to(message, "Некорректный формат времени. Используйте, например, 10m, 2h или 5d")
                return

            # Проверяем, есть ли ответ на сообщение
            if message.reply_to_message:
                target_user_id = message.reply_to_message.from_user.id
                chat_id = message.chat.id

                # Мутим пользователя
                bot.restrict_chat_member(chat_id, target_user_id, can_send_messages=False)

                # Костыль для определения юзернейма
                usernameToMute = message.reply_to_message.from_user.username

                if usernameToMute == None or usernameToMute == "":
                    usernameToMute = "USERNOTHAVEUSERNAME"

                # Сохраняем в бд пользователя
                sq.mute_user(target_user_id, usernameToMute, mute_time, chat_id, reason)
                # Отправляем ответ
                bot.reply_to(message, f"Пользователь @{usernameToMute} замучен на {time_value} {time_unit}. Причина: {reason}")
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить.")
        
        except:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(commands=['unmute'])
    def unmute_command(message):
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
        
            usernameToMute = message.reply_to_message.from_user.username

            if usernameToMute == None or usernameToMute == "":
                usernameToMute = "USERNOTHAVEUSERNAME"

            sq.unmute_user(message.reply_to_message.from_user.id, message.chat.id)
            bot.restrict_chat_member(
                message.chat.id, message.reply_to_message.from_user.id,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True)
            bot.reply_to(message, f"Пользователь @{usernameToMute} был размучен")
        except:
            d.send_view_traceback(message, traceback.format_exc())
    
def mute(user_id, chatid, reason, username, time):
    bot_g.restrict_chat_member(chatid, user_id, can_send_messages=False)
    bot_g.send_message(chatid, f"Пользователь {username} замучен на {time}. Причина: {reason}")

def unmute(user_id, chatid):
    bot_g.restrict_chat_member(
        chatid, user_id,
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True)
