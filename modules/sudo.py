from telebot.types import ReactionTypeEmoji
import config
from modules import auth
from modules import botdebug as d
import traceback
import time

def setup_handlers(bot):

    @bot.message_handler(commands=['sudo'])
    def sudo(message):
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

            args = message.text.split()
            
            if len(args) <= 3:
                bot.reply_to(message, "Недостаточно аргументов.\nИспользование: /sudo bot действие сообщение")
                return

            full_message = ""
            index = 0

            if args[1] == "bot" and args[2] == "sendMessage":
                for i in args:
                    if index <= 2:
                        pass
                    else:
                        full_message += i + " "
                    index += 1
                bot.send_message(config.group_chatid, full_message)
            elif args[1] == "bot" and args[2] == "replyToMessage":
                if len(args) <= 4:
                    bot.reply_to(message, "Недостаточно аргументов.\nИспользование: /sudo bot replyToMessage {messageId} сообщение")
                    return

                for i in args:
                    if index <= 3:
                        pass
                    else:
                        full_message += i + " "
                    index += 1

                bot.send_message(config.group_chatid, full_message, reply_to_message_id=int(args[3]))
            else:
                bot.reply_to(message, "Неверный аргумент от кого.")
                return

            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)
        except:
            d.send_view_traceback(message, traceback.format_exc())