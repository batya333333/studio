from django.contrib import admin
from .models import Master, Order, Appointment
from django.utils import timezone

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone', 'email', 'service', 'date', 'time', 'status'
    )
    list_filter = ('service', 'date', 'status')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    def confirm_appointments(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'Подтверждено {updated} записей.')
    confirm_appointments.short_description = "Подтвердить выбранные записи"

    def cancel_appointments(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(
            status='cancelled',
            cancelled_at=timezone.now()
        )
        self.message_user(request, f'Отменено {updated} записей.')
    cancel_appointments.short_description = "Отменить выбранные записи"

    def complete_appointments(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'confirmed']).update(status='completed')
        self.message_user(request, f'Отмечено как выполнено {updated} записей.')
    complete_appointments.short_description = "Отметить как выполненные"
admin.site.register(Master)
admin.site.register(Order)
