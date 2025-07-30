from django import forms
from .models import Appointment
from datetime import datetime
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['first_name', 'last_name','date', 'time', 'phone', 'email']
        widgets = {
            'phone': forms.TextInput(attrs={
                'id': 'id_phone',
                'type': 'tel',
                'placeholder': '+7 (___) ___-__-__',
                'maxlength': '18',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'example@gmail.com',
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Если пользователь авторизован и имеет профиль, скрываем поля
        if user and user.is_authenticated:
            try:
                profile = user.profile
                # Убираем поля, которые есть в профиле
                if 'first_name' in self.fields:
                    del self.fields['first_name']
                if 'last_name' in self.fields:
                    del self.fields['last_name']
                if 'phone' in self.fields:
                    del self.fields['phone']
                if 'email' in self.fields:
                    del self.fields['email']
            except:
                # Если профиль не существует, оставляем все поля
                pass

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('+7') or not phone[1:].isdigit() or len(phone) != 12:
            raise forms.ValidationError('Телефон должен быть в формате +7XXXXXXXXXX')
        return phone
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now():
            raise forms.ValidationError('Дата не может быть в прошлом')
        return date
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith(('@gmail.com', '@mail.ru', '@yandex.ru')):
            raise forms.ValidationError('Email должен быть на gmail.com, mail.ru или yandex.ru')
        return email
