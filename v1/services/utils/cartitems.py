from django.shortcuts import get_object_or_404
from carts.models import CartItem
from services.utils.cart import save_cart
from asgiref.sync import sync_to_async

# Convert the product creation function into an async callable
@sync_to_async
def create_cartitem(product, cart):
    """
    This function creates a cart item for a specific product and cart.
    If the cart item already exists, the quantity is increased by one. 
    The cart is then saved to the database.

    """
    cartitem, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        size='M',
        color='Black',
    )
    if created:
        pass
    else:
        cartitem.quantity += 1
    cartitem.save()
        
   
    return cartitem

@sync_to_async
def get_cart_items(cart):
    """This function retrieves all cart items for a specific cart."""
    return list(cart.items.select_related('product').all())

@sync_to_async
def get_cart_item_details(item):
    """This function retrieves the details of a specific cart item in a cart object."""
    return {
        'id': item.pk,
        'product': item.product.name,
        'quantity': item.quantity,
        'size': item.size,
        'color': item.color,
        'product_url': f'/products/{item.product.item_id}',
        'available_size': item.product.available_sizes,
        'available_color': item.product.available_colors,
        'price': item.product.price,
        'total_price': item.total_price
    }

async def get_cart_items_details(cart_items):
    """This function retrieves the details of all cart items in a cart object."""
    return [await get_cart_item_details(item) for item in cart_items]


@sync_to_async
def get_cartitem(pk):
    """This function retrieves a specific cart item by its primary key."""
    return get_object_or_404(CartItem, pk=pk)

@sync_to_async
def save_cartitem(cartitem):
    """This function saves a cart item to the database."""
    cartitem.save()

@sync_to_async
def delete_cartitem(cartitem):
    """This function saves a cart item to the database."""
    cartitem.delete()























# async def get_cartitem(pk):
#     return await sync_to_async(CartItem.objects.get)(pk=pk)

async def update_cartitem(pk, fields):
    cartitem = CartItem.objects.filter(pk=pk).update(**fields)
    return cartitem



