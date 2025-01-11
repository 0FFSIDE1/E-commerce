from django.http import JsonResponse
from django.shortcuts import redirect, render
from carts.models import Cart
from customers.models import Customer
from orders.models import Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from app.tasks import admin_send_email
from services.utils.cart import clear_cart
from services.utils.user import add_user_to_cart, staff_required
from services.emails.utils.context import context

# Create your views here.
import logging
logger = logging.getLogger(__name__)

@login_required
@user_passes_test(staff_required,  login_url='login', redirect_field_name='login')
def UpdateOrderView(request, pk):
    if request.method == 'POST':
        status = request.POST.get('status', None)
        if status is None:
            messages.error(request, 'Status cannot be None, Provide Order status!')
            return redirect('order-detail', pk)
        else:
            
        
            try:
                order = Order.objects.get(order_id=pk)
                print(order)
                order.status = status
                context_data = context(order=order)
                if status == 'Pending':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Order Processing: # {order.order_id}', body='emails/order_pending.html')
                    print(f'Task queued: {result}')
            
                if status == 'Paid':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Payment Receipt #{order.order_id}', body='emails/payment_success.html')
                    print(f'Task queued: {result}')
            
                if status == 'Shipped':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Order {status}: #{order.order_id}', body='emails/order_shipped.html')
                    print(f'Task queued: {result}')
                
                if status == 'Delivered':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Order {status}: #{order.order_id}', body='emails/order_delivered.html')
                    print(f'Task queued: {result}')
                
                if status == 'Cancelled':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Order {status}: #{order.order_id}', body='emails/order_cancelled.html')
                    print(f'Task queued: {result}')
                
                order.save()

                messages.success(request, 'Order updated successfully!')
                return redirect('order-detail', pk)
            
            except Exception as e:
                messages.error(request, f'Updated Failed! {str(e)}')
                return redirect('order-detail', pk)


def CreateOrderView(request):
    logger.debug('Received request: %s', request)
    if request.method == 'POST':
        try:
            # Attempt to get customer and cart based on session key
            logger.debug('Attempting to get customer and cart for session_key: %s', request.session.session_key)
           
            customer = Customer.objects.get(session=request.session.session_key)
            logger.debug('Customer retrieved: %s', customer)
            
            cart = Cart.objects.get(session=customer.session)
            logger.debug('Cart retrieved: %s', cart)
           

            # Create the order
            order = Order.objects.create(customer=customer, cart=cart)
            logger.debug('Order created: %s', order)
            

            # Generate invoice context
            invoice = context(order=order)
           
            logger.debug('Generated invoice: %s', invoice)

            try:
                # Attempt to send the invoice email
                result = admin_send_email.delay(context=invoice, to_email=customer.email, subject=f'Invoice for your order #{order.order_id}', body='emails/invoice.html')
                logger.debug(f'Task queued for sending email: {result}')
               
                clear_cart(cart)
                logger.debug('Cart cleared after order creation')

            except Exception as email_error:
                logger.error(f'Error sending invoice email: {str(email_error)}')
                

            return JsonResponse({'success': True, 'order_id': order.order_id, 'amount': order.total_amount})

        except Exception as e:
            logger.error(f'Error processing order: {str(e)}')
            
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    else:
        logger.warning('Invalid request method: %s', request.method)
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)