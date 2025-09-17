from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """Форма для редактирования личной информации"""
    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            return email
        # Проверяем уникальность email среди пользователей, исключая текущего
        user_qs = User.objects.filter(email__iexact=email)
        if self.instance and getattr(self.instance, 'user_id', None):
            user_qs = user_qs.exclude(id=self.instance.user_id)
        if user_qs.exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Синхронизация с моделью User
        user = profile.user
        # Имена
        user.first_name = (profile.first_name or '').strip()
        user.last_name = (profile.last_name or '').strip()
        # Email и username синхронизируем по email профиля
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if email:
            user.email = email
            user.username = email
        if commit:
            user.save()
            profile.save()
        return profile
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
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
