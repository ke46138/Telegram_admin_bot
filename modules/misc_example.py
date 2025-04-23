from config import admins_usernames, channel_id, advert_text
from modules import botdebug as d
import traceback

def setup_misc_handlers(bot):

    @bot.message_handler(commands=['admins'])
    def who_is_admin(message):
        try:
            bot.reply_to(message, admins_usernames, parse_mode='HTML')
        except:
            d.send_view_traceback(message, traceback.format_exc())
        

    def from_specific_channel(message):
        return message.sender_chat and message.sender_chat.id == channel_id

    @bot.message_handler(func=from_specific_channel, content_types=['text', 'photo', 'video', 'audio', 'document', 'sticker', 'voice', 'video_note', 'animation', 'contact', 'location', 'poll'])
    def advert(message):
        try:
            bot.unpin_chat_message(message.chat.id, message.id)
            bot.reply_to(message, advert_text, parse_mode='HTML', disable_web_page_preview=True)
        except:
            d.send_view_traceback(message, traceback.format_exc())