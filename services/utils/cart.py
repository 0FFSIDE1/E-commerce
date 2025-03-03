from carts.models import Cart
from customers.models import Customer
from asgiref.sync import sync_to_async


@sync_to_async
def get_cart(user, session):
    """
    Retrieve or create a cart for a customer or an anonymous user.

    Args:
        user: The HTTP request object (used for anonymous users).
        session: A Customer object (used for logged-in users).

    Returns:
        Cart object for the specified customer or session.

    Raises:
        ValueError: If neither request nor customer is provided.
    """
    if not user and not session:
        raise ValueError("Either 'request' or 'customer' must be provided to retrieve or create a cart.")

    try:
        
        cart, created = Cart.objects.get(user=user)
       
        return cart

    except Exception as e:
        # Retrieve or create a cart for a anonymous user, session_id is being controlled by signal
        cart = Cart.objects.get_or_create(session=session)

        return cart[0]
    except Cart.DoesNotExist:
        # Retrieve or create a cart for a anonymous user, session_id is being controlled by signal
        # customer = Customer.objects.get(session=session)
        # cart = Cart.objects.get(customer=customer.session)
        cart = Cart.objects.get_or_create(session=session)


        return cart[0]
    
   


@sync_to_async
def get_cart_by_customer(customer):
    """This function gets  or create a based on logged user"""
    cart = Cart.objects.get(user=customer)
    
    return cart
   

@sync_to_async
def get_cart_by_session(session_key):
    """This function gets or create cart based on a session for anonymous user"""
    
    cart = Cart.objects.get_or_create(session=session_key)
    
    return cart[0]


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

