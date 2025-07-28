from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """Форма для редактирования личной информации"""
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """Форма для смены пароля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка полей формы
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Введите текущий пароль'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Введите новый пароль'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Подтвердите новый пароль'})
