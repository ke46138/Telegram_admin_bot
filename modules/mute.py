from datetime import timedelta
from modules import sqlite_adapter as sq
from config import admins, allowed_chats
from modules import botdebug as d
import traceback

bot_g = ""

def setup_mute_handlers(bot):
    """Регистрируем обработчик команды /mute"""
    
    bot_g = bot

    @bot.message_handler(commands=['mute'])
    def mute(message):
        #user_id = message.from_user.id  # ID того, кто вызывает команду
        if message.sender_chat:
            user_id = message.sender_chat.id
        elif message.from_user:
            user_id = message.from_user.id
        else:
            bot.reply_to(message, "Ошибка: не удалось определить отправителя. ПОЗДРАВЛЯЮ, КАК ТЫ ЭТО СДЕЛАЛ?")
            return
        #print(user_id)
        # Проверяем, есть ли пользователь в списке разрешённых
        if user_id not in admins and user_id not in allowed_chats:
            bot.reply_to(message, "У вас нет прав на использование этой команды")
            return

        try:
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

                # Сохраняем в бд пользователя
                sq.mute_user(target_user_id, message.reply_to_message.from_user.username, mute_time, chat_id, reason)
                # Отправляем ответ
                bot.reply_to(
                    message,
                    f"Пользователь @{message.reply_to_message.from_user.username} замучен на {time_value} {time_unit}. Причина: {reason}"
                )
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить.")
        
        except Exception as e:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(commands=['unmute'])
    def unmute_command(message):
        if message.sender_chat:
            user_id = message.sender_chat.id
        elif message.from_user:
            user_id = message.from_user.id
        else:
            bot.reply_to(message, "Ошибка: не удалось определить отправителя")
            return
        
        if user_id not in admins and user_id not in allowed_chats:
            bot.reply_to(message, "У вас нет прав на использование этой команды")
            return
        
        try:
            sq.unmute_user(message.reply_to_message.from_user.id, message.chat.id)
            bot.restrict_chat_member(
                message.chat.id, message.reply_to_message.from_user.id,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был размучен")
        except Exception as e:
            d.send_view_traceback(message, traceback.format_exc())
    
def mute(user_id, chatid, reason, username, time):
    print(9)
    bot_g.restrict_chat_member(chatid, user_id, can_send_messages=False)
    print(10)
    bot_g.send_message(chatid, f"Пользователь {username} замучен на {time}. Причина: {reason}")
    print(11)

def unmute(user_id, chatid):
    bot_g.restrict_chat_member(
        chatid, user_id,
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True)
