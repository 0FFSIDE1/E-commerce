from rest_framework import status
from rest_framework.generics import (GenericAPIView, ListAPIView, CreateAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response
from .models import CartItem, Product, Cart
from services.utils.cart import get_or_create_cart, get_product_or_404
from services.serializers.cart import CartItemSerializer
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics



class SnippetList(mixins.ListModelMixin, 
                  mixins.CreateModelMixin, 
                  generics.GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Determine the customer or session ID
        customer = request.data.get("customer") if request.user.is_authenticated else None
        session_id = request.session.get("cart_session_id")
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        # Validate product presence
        if not product_id:
            return Response({"error": "Product is required."}, status=status.HTTP_400_BAD_REQUEST)

        # If the user is not authenticated, ensure session ID exists
        if not customer and not session_id:
            session_id = uuid4().hex  # Generate a new session ID
            request.session["cart_session_id"] = session_id

        try:
            # Ensure the product exists
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Retrieve or create the cart
            if customer:
                cart, created = Cart.objects.get_or_create(customer_id=customer)
            else:
                cart, created = Cart.objects.get_or_create(session_id=session_id)

            # Check if the product already exists in the cart
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()

            if cart_item:
                # Update the existing cart item's quantity
                cart_item.quantity += int(quantity)
                cart_item.total_price = cart_item.quantity * product.price  # Assuming `price` field exists in Product
                cart_item.save()
                return Response(
                    {"message": "Cart item updated successfully.", "cart_item": CartItemSerializer(cart_item).data},
                    status=status.HTTP_200_OK,
                )
            else:
                # Create a new cart item
                new_cart_item = CartItem.objects.create(
                    cart=cart, product=product, quantity=quantity, total_price=int(quantity) * product.price
                )
                return Response(
                    {"message": "Cart item added successfully.", "cart_item": CartItemSerializer(new_cart_item).data},
                    status=status.HTTP_201_CREATED,
                )
        except Cart.DoesNotExist:
            return Response({"error": "Cart for the user or session could not be found or created."}, status=status.HTTP_400_BAD_REQUEST)
        
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


# class CartItemsView(ListAPIView):
#     """
#     View all cart items for a specific user (auth or non-auth) based on the ID.
#     """
#     serializer_class = CartItemSerializer

#     def get_queryset(self):
#         # Extract the ID from the URL, which could be a name, session ID, or any identifier
#         identifier = self.kwargs.get("pk")

#         # Attempt to find a cart associated with the given identifier (customer or session)
#         cart = Cart.objects.filter(customer=identifier).first() or Cart.objects.filter(session_id=identifier).first()

#         # If no cart is found, return an empty queryset
#         if not cart:
#             return CartItem.objects.none()

#         # Return all items associated with the found cart
#         return CartItem.objects.filter(cart=cart)

#     def list(self, request, *args, **kwargs):
#         # Get the queryset for the cart items
#         queryset = self.get_queryset()

#         # If the cart is empty or no cart is found, return a 404 with a custom message
#         if not queryset.exists():
#             return Response({"message": "Your cart is empty or does not exist."}, status=status.HTTP_404_NOT_FOUND)

#         # Serialize and return the cart items
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class AddOrUpdateCartItemView(CreateAPIView):
#     """
#     Add a new item to the cart or update the quantity if it already exists.
#     """
#     serializer_class = CartItemSerializer

#     def post(self, request, *args, **kwargs):
#         customer = request.data.get("customer")  # Authenticated user, optional
#         session_id = request.data.get("session_id")  # Anonymous session, optional
#         product_id = request.data.get("product")  # Product being added
#         quantity = int(request.data.get("quantity", 1))  # Default to 1

#         if not product_id:
#             return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Retrieve or create the cart for the current user or session
#             cart = get_or_create_cart(request=request, customer=customer, session_id=session_id)

#             # Check if the product exists
#             product = Product.objects.get(item_id=product_id)

#             # Strictly ensure cart item belongs to this cart
#             cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#             if created:
#                 # Add new item
#                 cart_item.quantity = quantity
#                 message = "Item added to the cart."
#             else:
#                 # Update quantity of existing item
#                 cart_item.quantity += quantity
#                 message = "Item quantity updated in the cart."

#             cart_item.save()

#             # Serialize and return the response
#             serializer = self.serializer_class(cart_item)
#             return Response({"message": message, "cart_item": serializer.data}, status=status.HTTP_201_CREATED)

#         except Product.DoesNotExist:
#             return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)



# class CheckProductInCartView(RetrieveUpdateAPIView):
#     """
#     Check if a product is in the customer's cart and update it if needed.
#     """
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer

#     def get_object(self):
#         # Retrieve the cart item for a specific customer and product
#         customer = self.request.data.get("customer")
#         product_id = self.request.data.get("product_id")

#         if not (customer and product_id):
#             raise ValueError("Both customer and product_id must be provided.")

#         try:
#             # Get the customer's cart
#             cart = Cart.objects.get(customer=customer)
#         except Cart.DoesNotExist:
#             raise ValueError("Cart for the specified customer does not exist.")

#         try:
#             # Check if the product exists in the cart
#             cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
#         except CartItem.DoesNotExist:
#             cart_item = None  # Product does not exist in the cart

#         return cart_item

#     def retrieve(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         if cart_item:
#             # Serialize the cart item
#             serializer = self.serializer_class(cart_item)
#             return Response({"exists": True, "cart_item": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)

#     def update(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         if not cart_item:
#             return Response({"error": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)

#         # Update the cart item using the serializer
#         serializer = self.serializer_class(cart_item, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({"message": "Cart item updated successfully.", "cart_item": serializer.data}, status=status.HTTP_200_OK)

# class RemoveCartItemView(GenericAPIView):
#     """
#     Remove a product from the cart.
#     """

#     def delete(self, request):
#         customer = request.data.get("customer")
#         product_id = request.data.get("product_id")

#         if not (customer and product_id):
#             return Response({"error": "Customer and Product ID are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             cart = Cart.objects.get(customer=customer)
#             cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
#             if cart_item:
#                 cart_item.delete()
#                 return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)
#         except Cart.DoesNotExist:
#             return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
