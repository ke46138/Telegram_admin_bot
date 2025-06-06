#!/usr/bin/python3
import config
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from modules import advert
from modules import auth
from modules import admin_misc
from modules import botdebug
from modules import ban
from modules import mute
from modules import sudo
from modules import ticker
from modules import sqlite_adapter as sq
from modules import warn
from modules import report
from modules import retrying
from modules import restrict
from modules import urlfilter
from modules import misc
#from modules import badwords_filter # расскоментировать для включения фильтра матов
#from modules import trololo
import threading
import traceback
import telebot
import time

bot = telebot.TeleBot(config.bot_token, parse_mode="HTML")
sq.init_tables()

@asynccontextmanager
async def lifespan(app: FastAPI):
    bot.remove_webhook()
    bot.set_webhook(url=config.webhook_url_full)
    yield
    bot.remove_webhook()

app = FastAPI(lifespan=lifespan)

@app.post(config.webhook_url)
async def webhook(request: Request):
    json_data = await request.json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return {"status": "ok"}

@bot.message_handler(commands=['venom'])
def venom(message):
    bot.send_chat_action(message.chat.id, 'choose_sticker')
    time.sleep(2)
    venom_m = bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEMG5pnnQkIt8VkTDrBR-tbfCVK2c7emwACcmkAAq8wqEjr0bROJ9IZHDYE", reply_to_message_id=message.message_id)
    time.sleep(30)
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(venom_m.chat.id, venom_m.message_id)

@bot.message_handler(commands=['rules'])
def send_rules(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(2)
        bot.reply_to(message, config.rules, parse_mode='HTML')
    except:
        botdebug.send_view_traceback(message, traceback.format_exc())

@bot.message_handler(commands=['update_rules'])
def update_rules(message):
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

        bot.edit_message_text(config.rules, config.group_chatid, config.rules_id, parse_mode='HTML')

        bot.reply_to(message, "Готово!")
    except:
        botdebug.send_view_traceback(message, traceback.format_exc())

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "Pong!")

@bot.message_handler(commands=['safe_ping'])
def safe_ping(message):
    retrying.safe_api_call(bot.reply_to, message, "Safe pong!")

@bot.message_handler(commands=['about'])
def about(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.reply_to(message, config.about_bot_text)

@bot.message_handler(commands=['suda_admins'])
def suda_admins(message):
    bot.reply_to(message, config.suda_admins_text)

@bot.message_handler(commands=['debug_misc'])
def debug(message):
    bot.reply_to(message, f"""
Mute ticker thread is alive: {mute_t.is_alive()}
Chatid {message.chat.id}, messge id: {message.id}
""")

@bot.message_handler(commands=['reload_config'])
def reload_config(message):
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

        config.reload()

        bot.reply_to(message, "Готово!")
    except:
        botdebug.send_view_traceback(message, traceback.format_exc())

ticker.bot_g = bot
mute.setup_mute_handlers(bot)
warn.setup_warn_handlers(bot)
report.setup_report_handlers(bot)
restrict.setup_handlers(bot)
botdebug.setup_handlers(bot)
ban.setup_handlers(bot)
sudo.setup_handlers(bot)
admin_misc.setup_handlers(bot)
advert.setup_handlers(bot)
#trololo.setup_handlers(bot)
misc.setup_misc_handlers(bot)
urlfilter.setup_urlfilter_handlers(bot)
#badwords_filter.setup_badwords_filter_handlers(bot) # расскоментировать для включения фильтра матов

if __name__ == "__main__":
    import uvicorn
    from sdnotify import SystemdNotifier
    notifier = SystemdNotifier()
    mute_t = threading.Thread(target=ticker.mute_ticker, daemon=True)
    warn_t = threading.Thread(target=ticker.unwarn_ticker, daemon=True)
    mute_t.start()
    notifier.notify('READY=1')
    uvicorn.run(app, host=config.host, port=config.port)
