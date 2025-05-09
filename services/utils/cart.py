from carts.models import Cart
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser


@sync_to_async
def get_cart(user=None, session=None):
    """
    Retrieve or create a cart for a logged-in user or an anonymous session.

    Args:
        user (User): The authenticated user object (None if the user is anonymous).
        session (str): The session ID for an anonymous user.

    Returns:
        Cart: The existing or newly created cart object.

    Raises:
        ValueError: If neither 'user' nor 'session' is provided.
    """
    if not user and not session:
        raise ValueError("Either 'user' or 'session' must be provided to retrieve or create a cart.")
    
    if user and isinstance(user, AnonymousUser):  # Handle anonymous users properly
        user = None

    if user:
        # Retrieve or create a cart for a logged-in user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    # Retrieve or create a cart for an anonymous user (session-based)
    cart, created = Cart.objects.get_or_create(session=session)
    return cart
    
   


@sync_to_async
def get_cart_by_customer(customer):
    """This function gets  or create a based on logged user"""
    cart = Cart.objects.get(user=customer)
    
    return cart
   

@sync_to_async
def get_cart_by_session(session_key):
    """This function gets or create cart based on a session for anonymous user"""
    
    cart, created = Cart.objects.get_or_create(session=session_key)
    
    return cart


@sync_to_async
def save_cart(user, session_key):
    """ This Function saves a cart"""
    try:
        '''Save a cart for registered user and logged in user'''
       
        cart = Cart.objects.get(user=user)
        
        cart.save()
        
    except Exception as e:
        '''Save a cart for anonymous customer, (for first time users)'''    
        cart = Cart.objects.get(session=session_key)

        cart.save()
    return cart   
   
@sync_to_async
def update_cart(cart):
    cart.save() 


def clear_cart(cart):
    """Clear a cart"""
    cart.items.all().delete()
    cart.total_amount = 0.00
    cart.save()
    data = 'Cart Cleared'
    return data



from django.db import transaction
from carts.models import Cart, CartItem
from products.models import Product

def get_or_create_cart(user=None, session_id=None, customer=None):
    if user and user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user, defaults={"customer": customer})
    elif session_id:
        cart, _ = Cart.objects.get_or_create(session=session_id)
    else:
        raise ValueError("Either user or session_id must be provided.")
    return cart

@transaction.atomic
def add_to_cart(user=None, session_id=None, customer=None, product_id=None, quantity=1, size=None, color=None):
    cart = get_or_create_cart(user=user, session_id=session_id, customer=customer)
    product = Product.objects.get(item_id=product_id)

    # Check if item already in cart
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        color=color,
        defaults={"quantity": quantity}
    )

    if not created:
        item.quantity += quantity

    item.total_price = item.quantity * product.price
    item.save()

    # Recalculate cart total
    cart.total_amount = cart.calculate_total_amount()
    cart.save()
    return item