from services.utils.cart import *
from services.utils.session import create_session_if_not_exists
from carts.models import *
from services.utils.cartitems import *
from services.utils.product import get_product
from django.http import JsonResponse
import logging
from services.utils.product import get_product
from django.db import transaction
from asgiref.sync import sync_to_async
from django.views.decorators.http import require_http_methods
import json


# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.
@sync_to_async
def commit_transaction():
    transaction.commit()

@sync_to_async
def atomic_block():
    with transaction.atomic():
        return True

@require_http_methods(["POST"])
async def AddToCart(request, pk):
    try:
        # Ensure the session exists
        session_key = await create_session_if_not_exists(request)
        
        # Use a transaction to ensure atomicity
        await atomic_block()
        
        # Fetch the cart
        cart = await get_cart(user=request.user, session=session_key)
        
        if not cart:
            logger.error(f"Cart not found.")
            raise ValueError("Cart not found.")
        
        # Fetch the product
        product = await get_product(pk=pk)
       
        if not product:
            logger.error("Product not found.")
            raise ValueError("Product not found.")
        
        # Check product availability
        if int(product.quantity) <= 0:
            logger.error("Product is out of stock.")
            raise ValueError("Product is out of stock.")
        
        # Add the product to the cart
        cartitem = await create_cartitem(product=product, cart=cart)
        if cartitem:
            logger.info("CartItem Created Successfully")
        else:
            logger.error("Error Creating CartItem")
            
        # save the cart to get the total amount of items in the cart, controlled by signal
        success = await save_cart(user=request.user, session_key=session_key)

        if success:
            logger.info("Cart Saved Successfully")
        else:
            logger.error("Error saving cart")

        

        logger.info(f"Product '{product.name}' added to cart successfully.")
        data = {
            'success': True,
            'message': f'{product.name} added to cart successfully!',
            'product': {
                'name': product.name,
                'quantity': product.quantity,
                'price': product.price,
            }
        }
        
        return JsonResponse(data, safe=True)
    
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        data = {'success': False, 'message': str(ve)}
        return JsonResponse(data, status=400)
    
    except Exception as e:
        logger.error(f"Error adding product to cart: {e}")
        data = {'success': False, 'message': 'An error occurred. Please try again.'}
        return JsonResponse(data, status=500)




@require_http_methods(["GET"])
async def GetCart(request):
    try:
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key if not user else None
        # customer = await get_customer(user=user, session=session_key)

        cart = await get_cart_by_customer(customer=user)
        

        if not cart:
            raise ValueError("Cart not found.")
        
        cart_items = await get_cart_items(cart)
       
        cart_items_details = await get_cart_items_details(cart_items)
        
        
        data = {
            'success': True,
            'message': 'Cart retrieved successfully',
            'cartitems': cart_items_details,
            'total_amount': cart.total_amount,
        
        }
        
        logger.info(f"Response data: {data}")
        return JsonResponse(data, safe=True, status=200)
    
    except Exception as e:
        cart = await get_cart_by_session(session_key=request.session.session_key)
        if not cart:
            raise ValueError("Cart not found.")
        
        cart_items = await get_cart_items(cart)
        cart_items_details = await get_cart_items_details(cart_items)
        data = {
            'success': True,
            'message': 'Cart retrieved successfully',
            'cartitems': cart_items_details,
            'total_amount': cart.total_amount,
        }
        logger.info(f"Response data: {data}")
        return JsonResponse(data, safe=True, status=200)
    except Cart.DoesNotExist:
        logger.error("Cart not found.")
        data = {'success': False, 'message': 'Cart not found.'}
        return JsonResponse(data, status=404)
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        data = {'success': False, 'message': str(ve)}
        return JsonResponse(data, status=400)

        
@require_http_methods(["PATCH"])
async def UpdateCartItem(request, pk):
    """
    Endpoint to update cart item quantity, size, color or and other related fields
    PATCH /api/v1/<pk>/update-cart
    """
    try:
        cartitem = await get_cartitem(pk)
        data = json.loads(request.body)
        new_quantity = data.get('quantity')
        size = data.get('size')
        color = data.get('color')
        
      
        if new_quantity is not None :
            cartitem.quantity = new_quantity
        if size is not None:
            cartitem.size = size
        if color is not None:
            cartitem.color = color
        await save_cartitem(cartitem)

        # save the cart to ensure total amount is accurate
        cart = await save_cart(user=request.user, session_key=request.session.session_key)

        data = {
            "success": True,
            'total_amount': cart.total_amount, 
        }

        return JsonResponse(data, safe=True, status=200)
    except CartItem.DoesNotExist:
        return JsonResponse({"success": False, "message": "Cart item not found"}, status=404)
    
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_http_methods(["DELETE"])  
async def DeleteCartItem(request, pk):
    """
    Endpoint to delete cart item
    DELETE /api/v1/<pk>/delete
    """
    try:
        cartitem = await get_cartitem(pk=pk)
        
        await delete_cartitem(cartitem=cartitem)

        # save the cart to ensure total amount is accurate
        cart = await save_cart(user=request.user, session_key=request.session.session_key)
        data = {
            "success": True, 
            "message": "Product removed successfully",
            "total_amount": cart.total_amount,
        }
        return JsonResponse(data, safe=True)
    
    except CartItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Cart item not found"}, status=404)
    
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)



