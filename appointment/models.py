from django.db import models
from ivaskin.ivaapp.models import Forclient  # Импорт вашей модели услуги

class Appointment(models.Model):
    service = models.ForeignKey(Forclient, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    phone = models.IntegerField()  # Обязательное поле для телефона
    email = models.EmailField(blank=True)  # Необязательное поле для email

    def __str__(self):
        return f"{self.service} - {self.date} {self.time} - {self.phone}" 