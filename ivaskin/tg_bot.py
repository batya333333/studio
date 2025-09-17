import os
import django
import asyncio
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ivaskin.settings')
django.setup()

from appointment.models import AppointmentLog
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
    # Берём все свежие логи и шлём по мастеру из снимка
    logs = await sync_to_async(list)(
        AppointmentLog.objects.filter(created_at__gte=five_minutes_ago)
        .order_by('created_at')
    )
    for log in logs:
        chat_id = log.master_telegram_id
        if not chat_id:
            continue
        if log.action == 'created':
            header = 'Новая запись'
        elif log.action == 'rescheduled':
            header = 'Запись перенесена'
        elif log.action == 'cancelled':
            header = 'Запись отменена'
        elif log.action == 'status_changed':
            header = 'Статус обновлён'
        else:
            header = 'Обновление записи'

        parts = [
            f"{header}!",
            f"Услуга: {log.service_name or '-'}",
        ]
        
        # Форматируем дату и время
        def format_datetime(date_obj, time_obj):
            if not date_obj:
                return "не указано"
            date_str = date_obj.strftime("%d.%m.%Y")
            if time_obj:
                time_str = time_obj.strftime("%H:%M")
                return f"{date_str} {time_str}"
            return date_str
        
        if log.action in ('rescheduled',):
            old_datetime = format_datetime(log.old_date, log.old_time)
            new_datetime = format_datetime(log.new_date, log.new_time)
            parts.append(f"Старое время: {old_datetime}")
            parts.append(f"Новое время: {new_datetime}")
        else:
            datetime_str = format_datetime(log.new_date, log.new_time)
            parts.append(f"Дата и время: {datetime_str}")
            
        parts.extend([
            f"Клиент: {log.client_first_name or ''} {log.client_last_name or ''}",
            f"Телефон: {log.client_phone or '-'}",
            f"Email: {log.client_email or '-'}",
        ])
        if log.reason:
            parts.append(f"Причина: {log.reason}")

        text = "\n".join(parts)
        try:
            await bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

async def main():
    while True:
        await send_new_appointments()
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())