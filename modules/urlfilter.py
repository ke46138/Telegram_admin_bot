from urllib.parse import urlparse
import re
import config
import time
from modules import auth

def check_links_allowed(text: str) -> bool:
    """
    Проверяет, все ли ссылки в тексте принадлежат разрешённым доменам.
    
    :param text: Строка с текстом, содержащим ссылки.
    :param allowed_domains: Множество доменов, которые разрешены.
    :return: True, если все ссылки разрешены, иначе False.
    """
    url_pattern = re.compile(r'https?://[\w./?-]+')
    
    for match in url_pattern.findall(text):
        parsed_url = urlparse(match)
        domain = parsed_url.netloc

        if domain not in config.url_allowlist:
            return False
    
    return True

def setup_urlfilter_handlers(bot):
    
    @bot.message_handler(func=lambda message: True)
    def filter(message):
        allowed_links = check_links_allowed(message.text)
        if not allowed_links:
            result = auth.authorize(message)

            if result == -1:
                bot.reply_to(message, "Ошибка: не удалось определить отправителя. ПОЗДРАВЛЯЮ, КАК ТЫ ЭТО СДЕЛАЛ?")
                return
            elif result == 1:
                return

            warn_message = bot.reply_to(message, "Запрещённая ссылка!")
            time.sleep(1)
            bot.delete_message(message.chat.id, message.message_id)
            time.sleep(10)
            bot.delete_message(warn_message.chat.id, warn_message.message_id)
