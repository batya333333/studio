import os
import django
import asyncio
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ivaskin.settings')
django.setup()

from appointment.models import Appointment
from telegram import Bot
from django.utils import timezone
from datetime import timedelta

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения!")

bot = Bot(token=TELEGRAM_TOKEN)

async def send_new_appointments():
    now = timezone.now()
    five_minutes_ago = now - timedelta(minutes=5)
    # Оптимизация: select_related
    new_appointments = await sync_to_async(list)(
        Appointment.objects.filter(created_at__gte=five_minutes_ago).select_related('master', 'service')
    )
    for appointment in new_appointments:
        master = appointment.master
        service = appointment.service
        if master and master.telegram_id:
            text = (
                f"Новая запись!\n"
                f"Услуга: {service}\n"
                f"Дата: {appointment.date}\n"
                f"Время: {appointment.time}\n"
                f"Клиент: {appointment.first_name} {appointment.last_name}\n"
                f"Телефон: {appointment.phone}\n"
                f"Email: {appointment.email or 'не указан'}"
            )
            try:
                await bot.send_message(chat_id=master.telegram_id, text=text)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

async def main():
    while True:
        await send_new_appointments()
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())