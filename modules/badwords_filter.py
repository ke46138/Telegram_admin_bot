from config import admins, allowed_chats, badwords_filter_blacklist
import string
from transliterate import translit
import modules.badwords as words
from modules import sqlite_adapter
from modules import mute

def find_badwords(message):
    text = message.lower()

    # неплохие слова
    for w in words.not_bad_words:
        text = text.replace(w, '')

    # пунктуация
    for p in string.punctuation + ' ':
        text = text.replace(p, '')

    or_text = text
        
    # транслирование (slovo -> слово)
    text = translit(text, 'ru')
        
    for word in words.bad_words:
        if word in text:
            return True

        # похожие буквы
    for k, w in words.en_ru_map.items():
        text = text.replace(k, w)
        
    for word in words.bad_words:
        if word in text:
            return True

    text = or_text

    # похожие буквы
    for k, w in words.en_ru_map.items():
        text = text.replace(k, w)
        
    for word in words.bad_words:
        if word in text:
            return True
            
    return False

def setup_badwords_filter_handlers(bot):
    """Регистрируем обработчик фильтра плохих слов"""

    @bot.message_handler(func=lambda message: True)
    def filter(message):
        try:
            #print(1)
            result = find_badwords(message.text)
            #print(message.from_user.username)
            if result and message.from_user.id not in badwords_filter_blacklist:
                print(2)
                r = sqlite_adapter.add_warn(message.from_user.id, message.from_user.username, message.chat.id, "Мат")
                print(13)
                bot.reply_to(message, f'Не матерись, варн {r}/15')
                print(15)
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {str(e)}")
            print(e.with_traceback())