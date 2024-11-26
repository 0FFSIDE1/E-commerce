from rest_framework import status
from rest_framework.response import Response
from .models import CartItem
from services.utils.cart import get_cart
from services.utils.customer import get_customer
from services.serializers.cart import CartItemSerializer, CartSerializer
from django.shortcuts import get_object_or_404
from products.models import Product
# create your views here

async def add_to_cart(request, name):
    """
    Add a product to the cart.

    Args:
        request: The HTTP request object.
        name: The name of the product to add.

    Returns:
        Response object with appropriate status code.
    """
    if request.method != 'POST':
        return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        # Fetch the product
        product = get_object_or_404(Product, name=name)

        # Retrieve the customer
        customer = await get_customer(user=request.user)

        # Retrieve or create the cart
        cart = await get_cart(request=request, customer=customer)

        # Add the product to the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': request.POST.get('quantity', 1)}  # Default quantity to 1 if not provided
        )

        # If the cart item already exists, update the quantity
        if not created:
            cart_item.quantity += int(request.POST.get('quantity', 1))
            cart_item.save()

        return Response({'message': 'Product added to cart successfully.',
                         'CartItem': CartItemSerializer(cart_item),}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

