from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Appointment, AppointmentLog


def _snapshot(appointment: Appointment):
    return {
        'client_first_name': appointment.first_name,
        'client_last_name': appointment.last_name,
        'client_phone': appointment.phone,
        'client_email': appointment.email,
        'service_name': str(appointment.service) if appointment.service_id else None,
        'master_name': str(appointment.master) if appointment.master_id else None,
        'master_telegram_id': appointment.master.telegram_id if appointment.master_id else None,
    }


@receiver(post_save, sender=Appointment)
def log_appointment_created(sender, instance: Appointment, created, **kwargs):
    if created:
        snap = _snapshot(instance)
        AppointmentLog.objects.create(
            appointment=instance,
            action='created',
            new_date=instance.date,
            new_time=instance.time,
            new_status=instance.status,
            **snap,
        )


@receiver(pre_save, sender=Appointment)
def log_appointment_changes(sender, instance: Appointment, **kwargs):
    if not instance.pk:
        return
    try:
        prev = Appointment.objects.get(pk=instance.pk)
    except Appointment.DoesNotExist:
        return

    # Проверяем изменения
    date_time_changed = prev.date != instance.date or prev.time != instance.time
    status_changed = prev.status != instance.status

    if not (date_time_changed or status_changed):
        return

    snap = _snapshot(instance)

    # Определяем тип действия
    if status_changed and instance.status == 'cancelled':
        action = 'cancelled'
    elif date_time_changed and status_changed:
        action = 'rescheduled'  # Приоритет переносу, если изменились и время и статус
    elif date_time_changed:
        action = 'rescheduled'
    elif status_changed:
        action = 'status_changed'
    else:
        action = 'updated'

    # Создаем только один лог
    AppointmentLog.objects.create(
        appointment=instance,
        action=action,
        old_date=prev.date,
        old_time=prev.time,
        new_date=instance.date,
        new_time=instance.time,
        old_status=prev.status,
        new_status=instance.status,
        reason=instance.notes,
        **snap,
    )


