from carts.models import Cart
from products.models import Product
from rest_framework.exceptions import NotFound
from uuid import uuid4

# utils.py

from django.contrib.sessions.models import Session
from carts.models import Cart
from django.contrib.auth.models import User

def get_or_create_cart(request):
    if request.user.is_authenticated:
        # For authenticated users, get or create a cart associated with the user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # For unauthenticated users, store the cart in session
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()  # Create an anonymous cart
            request.session['cart_id'] = cart.id  # Save cart ID in session
    
    return cart

def get_product_or_404(product_id):
    try:
        return Product.objects.get(item_id=product_id)
    except Product.DoesNotExist:
        raise NotFound({"error": "Product not found."})
