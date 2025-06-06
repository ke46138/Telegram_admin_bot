import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import traceback

last_tb = "NO_TRACEBACK"
bot_g = ""

def send_view_traceback(message, tb):
    global last_tb
    markup = InlineKeyboardMarkup()
    tracebackyes = InlineKeyboardButton('Да', callback_data='tracebackyes')
    tracebackno = InlineKeyboardButton('Нет', callback_data='tracebackno')
    markup.add(tracebackyes, tracebackno)

    last_tb = tb.replace(config.bot_path, "*СТЁРТО*")
    print(last_tb)

    bot_g.send_message(message.chat.id, "Произошла ошибка. Багрепорт будет отправлен админу. Желаете посмотреть traceback?", reply_markup=markup)
    bot_g.send_message(config.report_admin_userid, f"Произошла ошибка при выполнении операции.\nTraceback:\n<blockquote expandable>{last_tb[-700:]}</blockquote>", parse_mode="HTML")

def setup_handlers(bot):

    global bot_g
    bot_g = bot

    @bot.message_handler(commands=['debug'])
    def debug(message):
        try:
            markup = InlineKeyboardMarkup()
            rules = InlineKeyboardButton('Правила', callback_data='rules')
            infounderpost = InlineKeyboardButton('Инфа под постом', callback_data='infounderpost')
            url_allowlist = InlineKeyboardButton('Белый список доменов', callback_data='urlallowlist')
            admin_list = InlineKeyboardButton('Список админов', callback_data='adminlist')
            thanks_list = InlineKeyboardButton('Доска благодарностей', callback_data='thankslist')
            markup.add(rules, infounderpost, url_allowlist, admin_list, thanks_list)

            bot.send_message(message.chat.id, "Что вы хотите отладить?", reply_markup=markup)
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {str(e)}")

    @bot.message_handler(commands=['manual_exception'])
    def manual_exception(message):
        try:
            raise Exception("TEST. IGNORE THIS")
        except:
            send_view_traceback(message, traceback.format_exc())

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == 'rules':
            bot.edit_message_text(config.rules, parse_mode='HTML', chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Готово!")
        elif call.data == 'infounderpost':
            bot.edit_message_text(config.advert_text, parse_mode='HTML', chat_id=call.message.chat.id, message_id=call.message.message_id, disable_web_page_preview=True)
            bot.answer_callback_query(call.id, "Готово!")
        elif call.data == 'urlallowlist':
            bot.edit_message_text(str(config.url_allowlist), chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Готово!")
        elif call.data == 'adminlist':
            bot.edit_message_text(config.admins_usernames, parse_mode='HTML', chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Готово!")
        elif call.data == 'thankslist':
            bot.edit_message_text(config.misc_thanks_post, parse_mode='HTML', chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Готово!")
        elif call.data == 'tracebackyes':
            global last_tb
            bot.edit_message_text(last_tb[-500:], chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Готово!")
        elif call.data == 'tracebackno':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.answer_callback_query(call.id, "Готово!")
        else:
            bot.edit_message_text("Нет такого callback запроса!", chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, "Нет такого callback запроса!")