from django.shortcuts import render, get_object_or_404, redirect
from appointment.models import Appointment
from appointment.forms import AppointmentForm
from ivaapp.models import Forclient
from datetime import datetime, time, timedelta
from django.utils import timezone
# Create your views here.

def get_time_slots(start, end, delta):
    slots = []
    current = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)
    while current < end_dt:
        slots.append(current.time())
        current += delta
    return slots

def book_appointment(request, service_id):
    service = get_object_or_404(Forclient, id=service_id)
    date_selected = request.POST.get('date') or request.GET.get('date')
    available_times = []
    date_obj = None
    if date_selected:
        try:
            date_obj = datetime.strptime(date_selected, '%Y-%m-%d').date()
            start_time = time(10, 0)
            end_time = time(20, 0)
            step = timedelta(minutes=30)
            all_slots = get_time_slots(start_time, end_time, step)
            taken = Appointment.objects.filter(service=service, date=date_obj).values_list('time', flat=True)
            available_times = [slot for slot in all_slots if slot not in taken]
        except Exception:
            available_times = []
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            if Appointment.objects.filter(service=service, date=date_obj, time=form.cleaned_data['time']).exists():
                form.add_error('time', 'Это время уже занято')
            else:
                appointment = form.save(commit=False)
                appointment.service = service
                appointment.date = date_obj
                appointment.save()
                return redirect('index')
    else:
        form = AppointmentForm()
    context = {
        'form': form,
        'service': service,
        'available_times': available_times,
        'date_selected': date_selected,
    }
    return render(request, 'appointment/book.html', context)
        
