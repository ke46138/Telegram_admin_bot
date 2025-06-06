from telebot.types import ReactionTypeEmoji
from modules import auth
from modules import botdebug as d
from modules import retrying
import traceback
import config

def setup_handlers(bot):

    @bot.message_handler(commands=['deploy_nav_post'])
    def deploy_nav_post(message):
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

            bot.send_message(config.group_chatid, config.misc_nav_post, parse_mode="HTML", disable_web_page_preview=True)

            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)
        except:
            d.send_view_traceback(message, traceback.format_exc())
    
    @bot.message_handler(commands=['update_nav_post'])
    def edit_nav_post(message):
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

            bot.edit_message_text(config.misc_nav_post, config.group_chatid, config.nav_post_id, parse_mode='HTML', disable_web_page_preview=True)

            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)
        except:
            d.send_view_traceback(message, traceback.format_exc())
    
    @bot.message_handler(commands=['deploy_advert'])
    def deploy_advert_post(message):
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

            reply_id = int(message.text[14:])
            #bot.send_message(config.group_chatid, config.advert_text, reply_to_message_id=reply_id, disable_web_page_preview=True, parse_mode='HTML')
            retrying.safe_api_call(bot.send_message, config.group_chatid, config.advert_text, reply_to_message_id=reply_id, disable_web_page_preview=True, parse_mode='HTML')

            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)
        except:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(commands=['set_desc'])
    def set_description(message):
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

            if len(args) < 2:
                bot.reply_to(message, "Недостаточно аргументов.\nИспользование: /set_desc описание")
                return

            full_message = ""
            index = 0

            for i in args:
                if index <= 0:
                    pass
                else:
                    full_message += i + " "
                index += 1

            bot.set_chat_description(config.group_chatid, full_message)

            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)
        except:
            d.send_view_traceback(message, traceback.format_exc())
    
    @bot.message_handler(commands=['deploy_thanks_post'])
    def deploy_thanks_post(message):
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

            bot.send_message(config.group_chatid, config.misc_thanks_post, parse_mode="HTML", disable_web_page_preview=True)

            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)
        except:
            d.send_view_traceback(message, traceback.format_exc())

    @bot.message_handler(commands=['update_thanks_post'])
    def update_thanks_post(message):
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

            bot.edit_message_text(config.misc_thanks_post, config.group_chatid, config.thanks_post_id, parse_mode='HTML', disable_web_page_preview=True)

            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)
        except:
            d.send_view_traceback(message, traceback.format_exc())