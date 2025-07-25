from django.db import models
from ivaapp.models import Forclient
from django.core.exceptions import ValidationError

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
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    service = models.ForeignKey(Forclient, on_delete=models.CASCADE, related_name='appoinments')
    date = models.DateTimeField()
    time = models.TimeField()
    phone = models.CharField(max_length=12, validators=[validate_phone])
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service} - {self.date} {self.time}"