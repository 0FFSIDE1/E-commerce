import json
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from services.utils.coupon import create_coupon
from services.utils.user import staff_required
from django.contrib import messages
import logging
from .models import Coupon
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from carts.models import Cart
from customers.models import Customer

# Create your views here.

logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(staff_required, login_url='login', redirect_field_name='login'), name='dispatch')
class AddCouponView(View):
    def post(self, request):
        try:
            # Get the data from form input
            name = request.POST['name']
            discount = request.POST['discount']
    
            # create the Coupon
            create_coupon(name=name, discount=discount)

            # Log successful Coupon creation
            logger.info(f"Coupon  created successfully.")
            messages.success(request, 'Coupon created successfully!')
            return redirect('coupons')

        except Exception as e:
            # Log the exception for debugging purposes
            logger.error(f"Error adding Coupon: {str(e)}")
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('coupons')



@login_required
@user_passes_test(staff_required,  login_url='login', redirect_field_name='login')
@csrf_exempt
def DeleteCouponView(request, pk):
    if request.method == 'POST':
        try:
            coupon = Coupon.objects.get(pk=pk)
            coupon.delete()
            messages.success(request, 'Coupon deleted successfully!')
            return JsonResponse({'success': True}, safe=True)
        except Exception as e:
            messages.error(request, f'Coupon deletion Failed! {str(e)}')
            return JsonResponse({'success': False}, safe=True)
        


def get_coupon_by_code(coupon_code):
    return Coupon.objects.get(code=coupon_code)

def save_cart(user, session_key):
    try:
        # customer = Customer.objects.get(user=user)
        cart, created = Cart.objects.get(user=user)
    except Exception as e:
        cart, created = Cart.objects.get_or_create(session=session_key)
    cart.save()
    return cart

def update_cart(new_amount, cart):
    Cart.objects.filter(cart_id=cart.cart_id).update(total_amount=new_amount)
    return cart.total_amount

def ApplyCouponView(request):
    if request.method == 'POST':
        try:
            cart = save_cart(user=request.user, session_key=request.session.session_key)
            data = json.loads(request.body)
            coupon_code = data.get('code')
            coupon = get_coupon_by_code(coupon_code)
            discount = coupon.discount
            discount_price = cart.total_amount * (discount / 100)
            new_total = cart.total_amount - discount_price
            update_cart(cart=cart, new_amount=new_total)
            return JsonResponse({'success': True, 'new_total': new_total, 'message': f'{coupon.coupon_name}: {coupon.discount}% Discount'}, safe=True,   status=200)
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Coupon does not exist'}, safe=True, status=404)
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart does not exist'}, safe=True, status=404)
        except Exception as e:
            
            return JsonResponse({'success': False, 'message': str(e)}, safe=True,   status=500)