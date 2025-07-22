from django import forms
from .models import Appointment
from datetime import datetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time', 'phone', 'email']


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('+7') or not phone[1:].isdigit() or len(phone) != 12:
            raise forms.ValidationError('Телефон должен быть в формате +7XXXXXXXXXX')
        return phone
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.now():
            raise forms.ValidationError('Дата не может быть в прошлом')
        return date
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith(('@gmail.com', '@mail.ru', '@yandex.ru')):
            raise forms.ValidationError('Email должен быть на gmail.com, mail.ru или yandex.ru')
        return email
