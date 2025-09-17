from django.db import models
from ivaapp.models import Forclient
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

def validate_phone(value):
    if not value.startswith('+7') or not value[1:].isdigit() or len(value) != 12:
        raise ValidationError('Телефон должен быть в формате +7XXXXXXXXXX')



class Master(models.Model):
    name = models.CharField(max_length=100)
    telegram_id = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Forclient, on_delete=models.CASCADE, related_name='orders')
    client_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    client_phone = models.CharField(max_length=20)
    client_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date} {self.time} - {self.client_name} {self.client_phone} ({self.service})'\

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
        ('rescheduled', 'Перенесена'),
    ]
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    service = models.ForeignKey(Forclient, on_delete=models.CASCADE, related_name='appoinments')
    date = models.DateTimeField()
    time = models.TimeField()
    phone = models.CharField(max_length=12, validators=[validate_phone])
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Поля для переноса записи:
    rescheduled_date = models.DateTimeField(blank=True, null=True)
    rescheduled_time = models.TimeField(blank=True, null=True)

    
    # Поля для отмены:
    cancelled_at = models.DateTimeField(blank=True, null=True)

    
    # Поля для логирования изменений:
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)  # Дополнительные заметки



    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service} - {self.date} {self.time} ({self.get_status_display()})"

    @property
    def is_active(self):
        """Проверяет, активна ли запись (не отменена и не выполнена)"""
        return self.status in ['pending', 'confirmed', 'rescheduled']
    
    @property
    def can_be_cancelled(self):
        """Можно ли отменить запись"""
        return self.status in ['pending', 'confirmed']

    @property
    def can_be_rescheduled(self):
        return self.status in ['pending', 'confirmed']

    
class AppointmentLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Создана'),
        ('rescheduled', 'Перенесена'),
        ('cancelled', 'Отменена'),
        ('status_changed', 'Статус изменён'),
        ('updated', 'Обновлена'),
    ]

    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    # Снимок клиентских данных на момент события
    client_first_name = models.CharField(max_length=50, blank=True, null=True)
    client_last_name = models.CharField(max_length=50, blank=True, null=True)
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    client_email = models.EmailField(blank=True, null=True)

    # Процедура и мастер на момент события
    service_name = models.CharField(max_length=255, blank=True, null=True)
    master_name = models.CharField(max_length=255, blank=True, null=True)
    master_telegram_id = models.CharField(max_length=100, blank=True, null=True)

    # Временные и статусные изменения
    old_date = models.DateTimeField(blank=True, null=True)
    old_time = models.TimeField(blank=True, null=True)
    new_date = models.DateTimeField(blank=True, null=True)
    new_time = models.TimeField(blank=True, null=True)
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.created_at} {self.get_action_display()} — {self.service_name} ({self.client_first_name} {self.client_last_name})"
