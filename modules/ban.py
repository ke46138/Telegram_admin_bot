from config import admins, allowed_chats
from modules import botdebug as d
import traceback

def setup_handlers(bot):

    @bot.message_handler(commands=['muteinf'])
    def infinity_mute(message):
        try:
            if message.sender_chat:
                user_id = message.sender_chat.id
            elif message.from_user:
                user_id = message.from_user.id
            else:
                bot.reply_to(message, "Ошибка: не удалось определить отправителя. ПОЗДРАВЛЯЮ, КАК ТЫ ЭТО СДЕЛАЛ?")
                return

            if user_id not in admins and user_id not in allowed_chats:
                bot.reply_to(message, "У вас нет прав на использование этой команды")
                return
            
            reason = message.text[9:] if message.text[9:] != '' else "Причина не указана"

            if message.reply_to_message:
                bot.restrict_chat_member(chat_id, target_user_id, can_send_messages=False)
                bot.reply_to(
                    message,
                    f"Пользователь @{message.reply_to_message.from_user.username} замучен навсегда. Причина: {reason}"
                )
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить навсегда.")

        except Exception as e:
            d.send_view_traceback(message, traceback.format_exc())
    
    @bot.message_handler(commands=['ban'])
    def ban_user(message):
        try:
            if message.sender_chat:
                user_id = message.sender_chat.id
            elif message.from_user:
                user_id = message.from_user.id
            else:
                bot.reply_to(message, "Ошибка: не удалось определить отправителя. ПОЗДРАВЛЯЮ, КАК ТЫ ЭТО СДЕЛАЛ?")
                return
            
            if user_id not in admins and user_id not in allowed_chats:
                bot.reply_to(message, "У вас нет прав на использование этой команды")
                return
            
            reason = message.text[5:] if message.text[5:] != '' else "Причина не указана"

            if message.reply_to_message:
                bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} забанен. Причина: {reason}")
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить.")
            
        except Exception as e:
            d.send_view_traceback(message, traceback.format_exc())
    
    @bot.message_handler(commands=['banid'])
    def ban_user_by_id(message):
        try:
            if message.sender_chat:
                user_id = message.sender_chat.id
            elif message.from_user:
                user_id = message.from_user.id
            else:
                bot.reply_to(message, "Ошибка: не удалось определить отправителя. ПОЗДРАВЛЯЮ, КАК ТЫ ЭТО СДЕЛАЛ?")
                return
            
            if user_id not in admins and user_id not in allowed_chats:
                bot.reply_to(message, "У вас нет прав на использование этой команды")
                return
            
            idtoban = 000000
            reason = "Причина не указана"

            msgwords = message.text.split()

            if not msgwords[1:1+1]:
                bot.reply_to(message, "Введите user id кого хотите забанить. Если ты не Кирилл, то спроси у него user id пользователя которого хочешь забанить")
                return

            if msgwords[2:2+1] != []:
                reason = msgwords[2]

            idtoban = msgwords[1]

            bot.ban_chat_member(message.chat.id, idtoban)
        except Exception as e:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(commands=['unban'])
    def unban_user(message):
        try:
            if message.sender_chat:
                user_id = message.sender_chat.id
            elif message.from_user:
                user_id = message.from_user.id
            else:
                bot.reply_to(message, "Ошибка: не удалось определить отправителя. ПОЗДРАВЛЯЮ, КАК ТЫ ЭТО СДЕЛАЛ?")
                return
            
            if user_id not in admins and user_id not in allowed_chats:
                bot.reply_to(message, "У вас нет прав на использование этой команды")
                return
            
            if message.reply_to_message:
                bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} разбанен.")
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить.")
            
        except Exception as e:
            d.send_view_traceback(message, traceback.format_exc())
