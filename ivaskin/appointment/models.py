from django.db import models
from ivaapp.models import Forclient
from django.core.exceptions import ValidationError

# Create your models here.

def validate_phone(value):
    if not value.startswith('+7') or not value[1:].isdigit() or len(value) != 12:
        raise ValidationError('Телефон должен быть в формате +7XXXXXXXXXX')

class Appointment(models.Model):
    service = models.ForeignKey(Forclient, on_delete=models.CASCADE, related_name='appoinments')
    date = models.DateTimeField()
    time = models.TimeField()
    phone = models.CharField(max_length=12, validators=[validate_phone])
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.service} - {self.date} - {self.time}"