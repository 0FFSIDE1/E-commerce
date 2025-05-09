from services.utils.cart import *
from carts.models import *
from services.utils.cartitems import *
import logging
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from carts.serializers import CartSerializer, UpdateCartItemSerializer, AddToCartSerializer, CartItemSerializer

# Set up logging
logger = logging.getLogger(__name__)

class AddToCartView(APIView):
    permission_classes = [permissions.AllowAny]  # Supports anonymous users

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = request.session.session_key or request.session.save() or request.session.session_key
        user = request.user if request.user.is_authenticated else None
        customer = getattr(user, 'customer', None) if user else None

        item = add_to_cart(
            user=user,
            session_id=session_id,
            customer=customer,
            product_id=serializer.validated_data['id'],
            quantity=serializer.validated_data['quantity'],
            size=serializer.validated_data.get('size'),
            color=serializer.validated_data.get('color'),
        )

        return Response({
            "success": True,
            "message": f"{item.product.name} {item.color} has been added to your cart.",
            "data": CartItemSerializer(item).data
        }, status=status.HTTP_201_CREATED)

class CartRetrieveView(APIView):
    def get(self, request):
        try:
            # Start atomic transaction to ensure data consistency
            with transaction.atomic():
                cart = None

                if request.user.is_authenticated:
                    cart, created = Cart.objects.select_related('user', 'customer') \
                        .prefetch_related('items__product') \
                        .get_or_create(user=request.user, defaults={'total_amount': 0.0})
                else:
                    # Ensure session exists
                    if not request.session.session_key:
                        request.session.create()
                    session_id = request.session.session_key

                    cart, created = Cart.objects.select_related('customer') \
                        .prefetch_related('items__product') \
                        .get_or_create(session=session_id, defaults={'total_amount': 0.0})

                serializer = CartSerializer(cart)
                return Response({'success': True, 'cart': serializer.data, 'message': 'Cart retrieved successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Failed to retrieve or create cart")
            return Response({
                'success': False,
                'error': 'Something went wrong while retrieving the cart.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartItemUpdateView(APIView):
    """
    PATCH /api/v1/cart-items/<pk>
    Updates a CartItem for both authenticated and anonymous users.
    """

    def patch(self, request, pk):
        try:
            # Retrieve the cart item
            cart_item = get_object_or_404(CartItem, pk=pk)
            serializer = UpdateCartItemSerializer(cart_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Recalculate the cart total
                cart = cart_item.cart
                cart.total_amount = cart.calculate_total_amount()
                cart.save()
                return Response({
                    "success": True,
                    "message": "Cart item updated successfully",
                    "cartItem": serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except CartItem.DoesNotExist:
            return Response({
                "success": False,
                "message": "Cart item not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                "success": False,
                "message": "An error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartItemDeleteView(APIView):
    def delete(self, request, pk):
        try:
            cart_item = get_object_or_404(CartItem, pk=pk)
            cart = cart_item.cart
            # Delete the cart item
            cart_item.delete()
            # Recalculate and save cart total
            cart.total_amount = cart.calculate_total_amount()
            cart.save()
            return Response({
                "success": True,
                "message": "Product removed successfully",
                "total_amount": cart.total_amount
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



