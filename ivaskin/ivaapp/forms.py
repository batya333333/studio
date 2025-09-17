from django import forms
from .models import Reviews
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import auth

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['serv', 'text']

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-select',
        'placeholder': 'Иван'
    }))
    last_name = forms.CharField(label='Фамилия', max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-select',
        'placeholder': 'Иванов'
    }))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={
        'class': 'form-select',
        'placeholder': 'name@example.com'
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-select',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-select',
        'placeholder': 'Повторите пароль'
    }))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email'].strip().lower()
        user.username = email
        user.email = email
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name = self.cleaned_data['last_name'].strip()
        if commit:
            user.save()
            # Ensure profile exists and stays in sync with user data
            try:
                profile = user.profile
            except Exception:
                # Fallback in case signal didn't create it yet
                from userprofile.models import Profile
                profile, _ = Profile.objects.get_or_create(user=user)
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.email = user.email
            profile.save()
        return user

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={
        'class': 'form-select',
        'placeholder': 'name@example.com'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-select',
        'placeholder': 'Введите пароль'
    }), required=True)

    def clean(self):
        cleaned = super().clean()
        email = (cleaned.get('email') or '').strip().lower()
        password = cleaned.get('password') or ''
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Неверный email или пароль')
        user = auth.authenticate(username=user.username, password=password)
        if not user:
            raise forms.ValidationError('Неверный email или пароль')
        self.user = user
        return cleaned

    def get_user(self):
        return getattr(self, 'user', None)
