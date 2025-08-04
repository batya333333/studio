from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import datetime, time, timedelta
from .models import Profile
from .forms import ProfileUpdateForm, CustomPasswordChangeForm
from appointment.models import Appointment, Master
from ivaapp.models import Forclient

def get_time_slots(start, end, delta):
    slots = []
    current = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)
    while current < end_dt:
        slots.append(current.time())
        current += delta
    return slots

@login_required
def profile_view(request):
    """Просмотр профиля пользователя с возможностью отмены и переноса записей"""
    profile = request.user.profile
    
    # Обработка отмены записи
    if request.method == 'POST' and 'cancel_appointment' in request.POST:
        appointment_id = request.POST.get('appointment_id')
        try:
            appointment = Appointment.objects.get(id=appointment_id, user=request.user)
            if appointment.can_be_cancelled:
                appointment.status = 'cancelled'
                appointment.cancelled_at = timezone.now()
                appointment.save()
                messages.success(request, 'Запись успешно отменена!')
            else:
                messages.error(request, 'Эту запись нельзя отменить.')
        except Appointment.DoesNotExist:
            messages.error(request, 'Запись не найдена.')
        return redirect('userprofile:profile')
    
    # Обработка переноса записи
    if request.method == 'POST' and 'reschedule_appointment' in request.POST:
        appointment_id = request.POST.get('appointment_id')
        new_date = request.POST.get('new_date')
        new_time = request.POST.get('new_time')
        
        try:
            appointment = Appointment.objects.get(id=appointment_id, user=request.user)
            if appointment.can_be_rescheduled and new_date and new_time:
                # Проверяем, что новая дата не в прошлом
                new_date_obj = datetime.strptime(new_date, '%Y-%m-%d').date()
                if new_date_obj < timezone.now().date():
                    messages.error(request, 'Дата не может быть в прошлом.')
                    return redirect('userprofile:profile')
                
                # Проверяем, что выбранное время доступно
                new_time_obj = datetime.strptime(new_time, '%H:%M').time()
                if Appointment.objects.filter(service=appointment.service, date=new_date_obj, time=new_time_obj).exists():
                    messages.error(request, 'Это время уже занято.')
                    return redirect('userprofile:profile')
                
                # Обновляем основную дату и время записи
                appointment.date = new_date_obj
                appointment.time = new_time_obj
                appointment.status = 'rescheduled'
                appointment.save()
                messages.success(request, 'Запись успешно перенесена!')
            else:
                messages.error(request, 'Эту запись нельзя перенести или не указана новая дата.')
        except Appointment.DoesNotExist:
            messages.error(request, 'Запись не найдена.')
        except ValueError:
            messages.error(request, 'Неверный формат даты или времени.')
        return redirect('userprofile:profile')
    
    # Получение записей
    appointments = Appointment.objects.filter(user=request.user).order_by('-date', '-time')
    active_appointments = appointments.filter(status__in=['pending', 'confirmed', 'rescheduled'])
    completed_appointments = appointments.filter(status__in=['completed', 'cancelled'])

    context = {
        'profile': profile,
        'active_appointments': active_appointments,
        'completed_appointments': completed_appointments,
        'total_appointments': appointments.count(),
    }

    return render(request, 'userprofile/profile.html', context)

@login_required
def get_available_times(request):
    """Получение доступных временных слотов для переноса записи"""
    from django.http import JsonResponse
    
    date_str = request.GET.get('date')
    appointment_id = request.GET.get('appointment_id')
    
    if not date_str or not appointment_id:
        return JsonResponse({'error': 'Не указана дата или ID записи'}, status=400)
    
    try:
        appointment = Appointment.objects.get(id=appointment_id, user=request.user)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Генерируем все возможные временные слоты
        start_time = time(10, 0)
        end_time = time(20, 0)
        step = timedelta(minutes=30)
        all_slots = get_time_slots(start_time, end_time, step)
        
        # Получаем занятые слоты для выбранной даты и услуги
        taken_slots = Appointment.objects.filter(
            service=appointment.service, 
            date=date_obj
        ).exclude(id=appointment_id).exclude(status='cancelled').values_list('time', flat=True)
        
        # Фильтруем доступные слоты
        available_slots = [slot.strftime('%H:%M') for slot in all_slots if slot not in taken_slots]
        
        return JsonResponse({
            'available_times': available_slots,
            'date': date_str
        })
        
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Запись не найдена'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'Неверный формат даты'}, status=400)
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
