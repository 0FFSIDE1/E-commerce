from carts.models import Cart
from products.models import Product
from rest_framework.exceptions import NotFound
from uuid import uuid4
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

def get_or_create_cart(request=None, customer=None, session_id=None):
    if not any([request, customer, session_id]):
        raise ValueError("Either request, customer, or session_id must be provided.")

    if customer:
        # Retrieve or create a cart for a specific user
        cart, created = Cart.objects.get_or_create(user=customer)
    elif request and request.user.is_authenticated:
        # Use authenticated user from request
        cart, created = Cart.objects.get_or_create(user=request.user)
    elif session_id:
        # Retrieve or create an anonymous cart using session ID
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    elif request:
        # Fallback to anonymous cart stored in session
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    else:
        raise ValueError("Insufficient data to create or retrieve cart.")

    return cart




def get_product_or_404(product_id):
    try:
        return Product.objects.get(item_id=product_id)
    except Product.DoesNotExist:
        raise NotFound({"error": "Product not found."})
