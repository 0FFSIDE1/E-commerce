from django.apps import AppConfig


class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carts'

    def ready(self):
        from services.signals.cart.customer_session_id import set_session_id
        import services.signals.cart.cartitem_total_price

