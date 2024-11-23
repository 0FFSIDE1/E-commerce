from django.apps import AppConfig


class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carts'

    def ready(self):
        import services.signals.customer.customer_session_id
