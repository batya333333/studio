import os
import django
import time
import asyncio
from asgiref.sync import sync_to_async


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ivaskin.settings')
django.setup()

from appointment.models import Appointment
from telegram import Bot
from django.utils import timezone
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TELEGRAM_TOKEN)

async def send_new_appointments():
    now = timezone.now()
    five_minutes_ago = now - timedelta(minutes=5)
    new_appointments = await sync_to_async(list)(
        Appointment.objects.filter(created_at__gte=five_minutes_ago)
    )
    for appointment in new_appointments:
        master = await sync_to_async(lambda a: a.master)(appointment)
        service = await sync_to_async(lambda a: a.service)(appointment)
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
            await bot.send_message(chat_id=master.telegram_id, text=text)

if __name__ == '__main__':
    while True:
        asyncio.run(send_new_appointments())
        time.sleep(60)