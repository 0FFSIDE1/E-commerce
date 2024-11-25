from django.apps import AppConfig


class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carts'

    def ready(self):
        from services.signals.cart import customer_session_id, cartitem_total_price

