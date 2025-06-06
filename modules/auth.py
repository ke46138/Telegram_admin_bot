import config

def authorize(message):
    """Функция для авторизации пользователей для использования админских функций.
    Не обрабатывает исключения.
    Возвращает:
    -1 - неопределён userid (это вообще может произойти?)
    1 - всё ок
    0 - access denied"""
    if message.sender_chat:
        user_id = message.sender_chat.id
    elif message.from_user:
        user_id = message.from_user.id
    else:
        return -1

    if user_id not in config.admins and user_id not in config.allowed_chats:
        return 0

    return 1