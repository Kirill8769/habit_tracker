import requests
from django.conf import settings


async def send_telegram_message(chat_id, message) -> bool:
    """Отправка напоминания через телеграм."""

    params = {
        'text': message,
        'chat_id': chat_id,
    }
    url = f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage'
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        return True
    return False
