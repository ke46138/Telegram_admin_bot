from modules import auth
from modules import botdebug as d
import traceback

def setup_handlers(bot):

    @bot.message_handler(commands=['muteinf'])
    def infinity_mute(message):
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

            reason = message.text[9:] if message.text[9:] != '' else "Причина не указана"
            userToMute = message.reply_to_message.from_user.username
            if userToMute == "" or userToMute == None:
                userToMute = "USERNOTHAVEUSERNAME"

            if message.reply_to_message:
                bot.restrict_chat_member(message.chat.id, message.reply_to_message.user.id, can_send_messages=False)
                bot.reply_to(
                    message,
                    f"Пользователь @{userToMute} замучен навсегда. Причина: {reason}"
                )
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить навсегда.")

        except:
            d.send_view_traceback(message, traceback.format_exc())
    
    @bot.message_handler(commands=['ban'])
    def ban_user(message):
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

            reason = message.text[5:] if message.text[5:] != '' else "Причина не указана"

            if message.reply_to_message:
                username = message.reply_to_message.from_user.username
                if username == "" or username == None:
                    username = "USERNOTHAVEUSERNAME"
                bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                bot.reply_to(message, f"Пользователь @{username} забанен. Причина: {reason}")
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить.")
            
        except:
            d.send_view_traceback(message, traceback.format_exc())
    
    @bot.message_handler(commands=['banid'])
    def ban_user_by_id(message):
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

            username = message.reply_to_message.from_user.username
            if username == "" or username == None:
                username = "USERNOTHAVEUSERNAME"
            bot.reply_to(message, f"Пользователь @{username} забанен. Причина: {reason}")
        except:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(commands=['unban'])
    def unban_user(message):
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
                if username == "" or username == None:
                    username = "USERNOTHAVEUSERNAME"
                bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                bot.reply_to(message, f"Пользователь @{username} разбанен.")
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, которого хотите замутить.")

        except:
            d.send_view_traceback(message, traceback.format_exc())
