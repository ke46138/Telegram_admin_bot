from urllib.parse import urlparse
import re
from config import url_allowlist, admins, allowed_chats, user_blacklist
import time

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
        
        if domain not in url_allowlist:
            return False
    
    return True


def setup_urlfilter_handlers(bot):
    
    @bot.message_handler(func=lambda message: True)
    def filter(message):
        allowed_links = check_links_allowed(message.text)
        if not allowed_links:
            if message.sender_chat:
                user_id = message.sender_chat.id
            elif message.from_user:
                user_id = message.from_user.id
            else:
                bot.reply_to(message, "Ошибка: не удалось определить отправителя")
                return
            if user_id not in admins and user_id not in allowed_chats and user_id not in user_blacklist:
                warn_message = bot.reply_to(message, "Запрещённая ссылка!")
                time.sleep(1)
                bot.delete_message(message.chat.id, message.message_id)
                time.sleep(10)
                bot.delete_message(warn_message.chat.id, warn_message.message_id)
