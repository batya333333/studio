from django.contrib import admin
from .models import Master, Order, Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone', 'email', 'service', 'date', 'time'
    )
    list_filter = ('service', 'date')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
admin.site.register(Master)
admin.site.register(Order)
