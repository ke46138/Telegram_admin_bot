from modules import sqlite_adapter as sq
from modules import auth
from modules import botdebug as d
import config
import time
import traceback

def setup_handlers(bot):

    @bot.message_handler(content_types=["new_chat_members"])
    def new_member(message):
        try:
            for new_member in message.new_chat_members:
                user_id = new_member.id
                sq.add_user(user_id, message.chat.id)
                bot.restrict_chat_member(
                    message.chat.id, message.from_user.id,
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True)
        except:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(content_types=['left_chat_member'])
    def member_left(message):
        user_id = message.left_chat_member.id
        sq.remove_user(user_id, message.chat.id)

    @bot.message_handler(commands=['only_admins'])
    def only_admins(message):
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

            result = sq.select_all_where('users_table', message.chat.id)
            muted_users_raw = sq.select_column_where('mute_table', 'id', message.chat.id)
            muted_users = [item[0] for item in muted_users_raw]

            for i in range(len(result)):
                if result[i][0] not in config.admins and result[i][0] not in config.allowed_chats and result[i][0] not in muted_users and result[i][0] not in config.user_blacklist:
                    bot.restrict_chat_member(message.chat.id, result[i][0], can_send_messages=False)
                time.sleep(0.1)
            
            bot.reply_to(message, 'Теперь писать могут только админы')
        except:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(commands=['all_users'])
    def all_users(message):
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
            
            result = sq.select_all_where('users_table', message.chat.id)
            muted_users_raw = sq.select_column_where('mute_table', 'id', message.chat.id)
            muted_users = [item[0] for item in muted_users_raw]

            for i in range(len(result)):
                if result[i][0] not in config.admins and result[i][0] not in config.allowed_chats and result[i][0] not in muted_users and result[i][0] not in config.user_blacklist:
                    bot.restrict_chat_member(
                            message.chat.id, result[i][0],
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_add_web_page_previews=True)
                time.sleep(0.1)

            bot.reply_to(message, 'Теперь писать могут все, кроме замученных пользователей')

        except:
            d.send_view_traceback(message, traceback.format_exc())