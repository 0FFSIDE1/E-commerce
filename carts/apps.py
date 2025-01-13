from django.apps import AppConfig


class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carts'


    def ready(self):
        from services.signals.cart.cart import set_session_id
        from services.signals.cart.cartitem import calculate_total_price_of_cartitem, recalculate_total_price


