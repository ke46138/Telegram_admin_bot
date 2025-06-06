import config
from modules import auth
from modules import botdebug as d
import traceback

def setup_report_handlers(bot):
# /report never gonna give you up
    @bot.message_handler(commands=['report'])
    def report(message):
        try:
            if message.reply_to_message:
                if message.reply_to_message.sender_chat:
                    user_id = message.sender_chat.id
                elif message.reply_to_message.from_user:
                    user_id = message.from_user.id
                else:
                    bot.reply_to(message, "Ошибка: не удалось определить отправителя")
                    return
                
                command_text = message.text
                report_text = ""

                if user_id == message.reply_to_message.from_user.id:
                    bot.reply_to(message, "Саморепорт запрещён")
                    return

                if user_id in config.admins or user_id in config.allowed_chats:
                    bot.reply_to(message, "Репорт админов запрещён")
                    return
                
                if message.reply_to_message.from_user.id == report_bot_id:
                    bot.reply_to(message, "Репорт бота запрещён")
                    return

                report_text = command_text.split(" ", 1)[1] if " " in command_text else "Не указано"

                message_text = message.reply_to_message.text

                bot.send_message(report_admin_userid, f"""
📢 <b>Новая жалоба</b>

От: @{message.from_user.username}
На: @{message.reply_to_message.from_user.username}
Текст сообщения: "{message_text}"
Ссылка на сообщение: <a href="https://t.me/c/{str(message.reply_to_message.chat.id)[4:]}/{message.reply_to_message.message_id}">Тыкъ</a>
Причина: {report_text}
""", parse_mode='HTML')

                bot.reply_to(message, f"На пользователя @{message.reply_to_message.from_user.username} был кинут репорт")
            else:
                bot.reply_to(message, "Вы должны ответить на сообщение пользователя, на которого хотите кинуть репорт")
        except:
            d.send_view_traceback(message, traceback.format_exc())