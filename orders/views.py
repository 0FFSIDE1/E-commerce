from collections import defaultdict
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from carts.models import Cart
from customers.models import Customer
from orders.models import Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from app.tasks import admin_send_email
from sellers.models import Vendor
from services.utils.cart import clear_cart
from services.utils.user import add_user_to_cart, staff_required, vendor_required
import logging
from services.email.context import context
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from services.serializers.order import OrderSerializer
from django.core.exceptions import PermissionDenied




logger = logging.getLogger(__name__)

# Create your views here.
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
                order.status = status
                context_data = context(order=order)
                if status == 'Pending':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Order Processing: # {order.order_id}', body='emails/order_pending.html')  
                if status == 'Paid':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Payment Receipt #{order.order_id}', body='emails/payment_success.html')
                if status == 'Shipped':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Order {status}: #{order.order_id}', body='emails/order_shipped.html')
                if status == 'Delivered':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Order {status}: #{order.order_id}', body='emails/order_delivered.html')
                if status == 'Cancelled':
                    result = admin_send_email.delay(context=context_data, to_email=order.customer.email, subject=f'Order {status}: #{order.order_id}', body='emails/order_cancelled.html')
                
                order.save()
                context = {
                    'success': True,
                    'message': 'Order created successfully'
                }
                return JsonResponse(context, safe=True)

            
            except Exception as e:
                context = {
                    'success': False,
                    'message': f'Error creating order {e}'
                }
                return JsonResponse(context, safe=True)
    else:
        context = {
                    'success': False,
                    'message': 'Method Not Allowed'
                }
        return JsonResponse(context, safe=True)



def CreateOrderView(request):
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
                # Attempt to send the invoice email to customer then clear the cart
                result = admin_send_email.delay(context=invoice, to_email=customer.email, subject=f'Invoice for your order #{order.order_id}', body='emails/invoice.html')
                logger.debug(f'Task queued for sending email: {result}')
                clear_cart(cart)
                logger.debug('Cart cleared after order creation')

               # Group order items by vendor
                vendor_items = defaultdict(list)  # Dictionary to group items by vendor
                for item in order.cart.items.all():  # Assuming Cart has related cart_items
                    vendor = item.product.vendor  # Assuming Product has a related vendor field
                    vendor_items[vendor].append({
                        'product_name': item.product.name,
                        'quantity': item.quantity,
                        'size': item.size,
                        'color': item.color,
                        'price': item.total_price,
                    })
            
                # Notify each vendor with their respective items
                for vendor, items in vendor_items.items():
                    vendor_email = vendor.email  # Assuming Vendor model has an `email` field
                    vendor_alert_context = {
                        'order_id': order.order_id,
                        'customer_name':  order.customer.first_name + ' ' + order.customer.last_name, 
                        'total_amount': order.total_amount,
                        'vendor_items': items,  # Include only the items related to this vendor
                        'created_at': order.created_at,
                        'status': order.status,
                    }
                    vendor_alert_result = admin_send_email.delay(
                        context=vendor_alert_context,
                        to_email=vendor_email,
                        subject=f'New order #{order.order_id} placed by {order.customer.first_name}',
                        body='emails/vendor_alert.html'
                    )
                    logger.debug(f'Task queued for sending email to vendor: {vendor_alert_result}')


            except Exception as email_error:
                logger.error(f'Error sending email: {str(email_error)}')

            return JsonResponse({'success': True, 'order_id': order.order_id, 'amount': order.total_amount, 'message': 'Order Created Successfully'})

        except Exception as e:
            logger.error(f'Error processing order: {str(e)}')
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    else:
        logger.warning('Invalid request method: %s', request.method)
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@require_http_methods(["GET"])
def CustomerOrder(request):
    try:
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Fetch the customer for the authenticated user
            customer = Customer.objects.get(user=request.user)
        else:
            # Handle anonymous user session
            session_key = request.session.session_key
            if not session_key:
                # Create a session for the anonymous user
                request.session.create()
                session_key = request.session.session_key

            # Fetch the customer based on the session
            customer = Customer.objects.get(session=session_key)

        # Fetch the orders for the customer
        orders = Order.objects.filter(customer=customer)
        
        serializer = OrderSerializer(orders, many=True)
        # Prepare the success response
        context = {
            'success': True,
            'message': 'Orders retrieved successfully',
            'orders': serializer.data,
        }
        return JsonResponse(context, status=200)

    except ObjectDoesNotExist:
        # Handle cases where the customer or orders are not found
        context = {
            'success': False,
            'message': 'No orders found for the customer',
        }
        return JsonResponse(context, status=404)

    except Exception as e:
        # Generic exception handling for unexpected errors
        context = {
            'success': False,
            'message': 'An unexpected error occurred. Please try again later.',
        }
        return JsonResponse(context, status=500)
    


@require_http_methods(["GET"])
def CustomerOrderDetail(request, pk):
    try:
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Fetch the customer for the authenticated user
            customer = Customer.objects.get(user=request.user)
        else:
            # Handle anonymous user session
            session_key = request.session.session_key
            if not session_key:
                # Create a session for the anonymous user
                request.session.create()
                session_key = request.session.session_key
           
            # Fetch the customer based on the session
            customer = Customer.objects.get(session=session_key)

        # Fetch the order for the customer
        order = Order.objects.get(order_id=pk, customer=customer)

        # Serialize the order data
        serializer = OrderSerializer(order)

        # Prepare the success response
        context = {
            'success': True,
            'message': 'Order retrieved successfully',
            'order': serializer.data,
        }
        return JsonResponse(context, status=200)

    except ObjectDoesNotExist:
        # Handle cases where the customer or order is not found
        context = {
            'success': False,
            'message': 'Order not found or you do not have access to it',
        }
        return JsonResponse(context, status=404)

    except Exception as e:
        # Generic exception handling for unexpected errors
        context = {
            'success': False,
            'message': 'An unexpected error occurred. Please try again later.',
        }
        return JsonResponse(context, status=500)
    

@login_required
@require_http_methods(["GET"])
@user_passes_test(vendor_required, login_url='login', redirect_field_name='login')
def VendorOrder(request):
    try:
        vendor_instance  = Vendor.objects.get(user=request.user)
        vendor_orders = Order.objects.filter(orderitems__product__vendor=vendor_instance).distinct()
        
        order = OrderSerializer(vendor_orders, many=True)
        
      
        context = {
            'success': True,
            'status': 'success',
            'message': 'Order Retrieved sucessfully',
            'order': order.data,
        }
        return JsonResponse(context,safe=True)

    except Exception as e:
        context = {
            'success': False,
            'status': 'error',
            'message': f'Error Retrieving Order {e}',
            
        }
        return JsonResponse(context,safe=True)
    

@login_required
@require_http_methods(["PATCH"]) 
@user_passes_test(vendor_required, login_url='login', redirect_field_name='login')
def VendorUpdateOrderItem(request, pk):

    try: 
        # parse the data from the request body
        data = json.loads(request.body)

        # Get the orderitem by id
        order_item = get_object_or_404(OrderItem, pk=pk)

        # Check if the logged-in vendor is allowed to update this order item
        vendor = request.user
        if order_item.product.vendor != vendor:
            raise PermissionDenied("You are not authorized to update this order item.")
        
        for field, value in data.items():
            if hasattr(order_item, field):
                setattr(order_item, field, value)
        
        order_item.save()

        # Return success response
        return JsonResponse({
            "message": "Order item updated successfully.",
            "order_item": {
                "id": order_item.id,
                "name": order_item.name,
                "size": order_item.size,
                "color": order_item.color,
                "price": str(order_item.price),
                "quantity": order_item.quantity,
                "total_price": str(order_item.total_price),
            }
        })
    
    except PermissionDenied as e:
        return JsonResponse({"error": str(e)}, status=403)
    
    except Exception as e:
        return JsonResponse({"error": "An error occurred."}, status=400)



