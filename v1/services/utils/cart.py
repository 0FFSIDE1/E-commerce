from carts.models import Cart
from products.models import Product
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist

async def get_cart(request=None, customer=None):
    """
    Retrieve or create a cart for a customer or an anonymous user.

    Args:
        request: The HTTP request object (used for anonymous users).
        customer: A Customer object (used for logged-in users).

    Returns:
        Cart object for the specified customer or session.

    Raises:
        ValueError: If neither request nor customer is provided.
    """
    if not (request or customer):
        raise ValueError("Either 'request' or 'customer' must be provided to retrieve or create a cart.")

    try:
        if customer:
            # Retrieve or create a cart for a specific customer
            cart, created = Cart.objects.get(customer=customer)
        elif request:
            # Retrieve or create a cart for a anonymous user, session_id is being controlled by signal
            cart = Cart.objects.get_or_create()
        return cart

    except ObjectDoesNotExist:
        raise ValueError("Unable to retrieve or create a cart.")




async def get_product_or_404(name):
    try:
        return Product.objects.get(name=name)
    except Product.DoesNotExist:
        raise NotFound({"error": "Product not found."})
