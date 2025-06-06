from telebot.apihelper import ApiTelegramException
import time

# * Костыль для нестабильного интернета
def safe_api_call(func, *args, max_retries=50, delay=3, **kwargs):
    print("Attempting to call Telegram API")
    for attempt in range(max_retries):
        try:
            func(*args, **kwargs)
            print("Telegram API call was successful")
            return 1
        except ApiTelegramException as e:
            print(f"[{attempt+1}/{max_retries}] Telegram API error: {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"[{attempt+1}/{max_retries}] Other error: {e}")
            time.sleep(delay)
    print("Telegram API call was unsuccessful")
    return 0