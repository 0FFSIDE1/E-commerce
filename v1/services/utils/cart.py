from carts.models import Cart
from products.models import Product
from rest_framework.exceptions import NotFound
from uuid import uuid4

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user)
    else:
        session_id = request.session.get("cart_session_id", None)
        if not session_id:
            session_id = str(uuid4())
            request.session["cart_session_id"] = session_id
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def get_product_or_404(product_id):
    try:
        return Product.objects.get(item_id=product_id)
    except Product.DoesNotExist:
        raise NotFound({"error": "Product not found."})
