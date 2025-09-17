from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment'

    def ready(self):
        # Импорт сигналов при старте
        try:
            import appointment.signals  # noqa: F401
        except Exception:
            # Не падаем на этапе миграций
            pass