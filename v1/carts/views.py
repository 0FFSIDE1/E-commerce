from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from .models import CartItem, Product, Cart
from services.utils.cart import get_or_create_cart
from services.serializers.cart import CartItemSerializer



class CartItemsView(ListAPIView):
    """
    View all cart items for a specific user (auth or non-auth) based on the ID.
    """
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # Extract the ID from the URL, which could be a name, session ID, or any identifier
        identifier = self.kwargs.get("pk")

        # Attempt to find a cart associated with the given identifier (customer or session)
        cart = Cart.objects.filter(customer=identifier).first() or Cart.objects.filter(session_id=identifier).first()

        # If no cart is found, return an empty queryset
        if not cart:
            return CartItem.objects.none()

        # Return all items associated with the found cart
        return CartItem.objects.filter(cart=cart)

    def list(self, request, *args, **kwargs):
        # Get the queryset for the cart items
        queryset = self.get_queryset()

        # If the cart is empty or no cart is found, return a 404 with a custom message
        if not queryset.exists():
            return Response({"message": "Your cart is empty or does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the cart items
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddOrUpdateCartItemView(CreateAPIView):
    """
    Add a new item to the cart or update the quantity if it already exists.
    """
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        customer = request.data.get("customer")
        session_id = request.data.get("session_id")
        product_id = request.data.get("item_id")  # Match the serializer field
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve or create a cart for the customer/session
            cart = get_or_create_cart(customer=customer, session_id=session_id)
            product = Product.objects.get(item_id=product_id)

            # Check if the cart item already exists
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if created:
                # If new, set the quantity
                cart_item.quantity = quantity
                message = "Item added to the cart."
            else:
                # If existing, increment the quantity
                cart_item.quantity += quantity
                message = "Item quantity updated in the cart."

            cart_item.save()

            # Serialize the updated cart item
            serializer = self.serializer_class(cart_item)
            return Response(
                {"message": message, "cart_item": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

class CheckProductInCartView(GenericAPIView):
    """
    Check if a product is in the customer's cart.
    """

    def get(self, request):
        customer = request.query_params.get("customer")
        product_id = request.query_params.get("product_id")

        if not (customer and product_id):
            return Response({"error": "Customer and Product ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(customer=customer)
            product_exists = CartItem.objects.filter(cart=cart, product_id=product_id).exists()
            return Response({"exists": product_exists}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)


class RemoveCartItemView(GenericAPIView):
    """
    Remove a product from the cart.
    """

    def delete(self, request):
        customer = request.data.get("customer")
        product_id = request.data.get("product_id")

        if not (customer and product_id):
            return Response({"error": "Customer and Product ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(customer=customer)
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if cart_item:
                cart_item.delete()
                return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
