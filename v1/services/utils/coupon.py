from coupon.models import Coupon
from asgiref.sync import sync_to_async


def create_coupon(name, discount):
    coupon = Coupon.objects.get_or_create(
        coupon_name=name,
        discount=discount,
    )
    
    return coupon

@sync_to_async
def get_coupon_by_code(code):
    """This function gets a coupon by code"""
    coupon = Coupon.objects.get(code=code)
    
    return coupon