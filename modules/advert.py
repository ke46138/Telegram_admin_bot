from modules import botdebug as d
from modules import retrying
import traceback
import config

def setup_handlers(bot):

    def from_specific_channel(message):
        return message.sender_chat and message.sender_chat.id == config.channel_id

    @bot.message_handler(func=from_specific_channel, content_types=['text', 'photo', 'video', 'audio', 'document', 'sticker', 'voice', 'video_note', 'animation', 'contact', 'location', 'poll'])
    def advert(message):
        try:
            retrying.safe_api_call(bot.unpin_chat_message, message.chat.id, message.id) # bot.unpin_chat_message(message.chat.id, message.id)
            retrying.safe_api_call(bot.reply_to, message, config.advert_text, parse_mode='HTML', disable_web_page_preview=True) # bot.reply_to(message, config.advert_text, parse_mode='HTML', disable_web_page_preview=True)
        except:
            d.send_view_traceback(message, traceback.format_exc())