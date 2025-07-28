from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from .forms import ProfileUpdateForm, CustomPasswordChangeForm

@login_required
def profile_view(request):
    """Просмотр профиля пользователя"""
    profile = request.user.profile
    return render(request, 'userprofile/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('userprofile:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'userprofile/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    """Смена пароля"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('userprofile:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'userprofile/change_password.html', {'form': form})