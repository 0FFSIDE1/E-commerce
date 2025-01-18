from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from services.signals.otp import generate_code
        from services.signals.subscription.generate_expire_date import generate_end_date
