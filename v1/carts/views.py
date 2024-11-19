from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from carts.models import Cart, CartItem
from products.models import Product
from services.utils.cart import get_or_create_cart

class Cart_View(APIView):
    def get(self, request):
        cart = get_or_create_cart(request)
        items = cart.items.all()
        cart_data = {
            "cart_id": cart.id,
            "items": [{"product": item.product.item_name, "quantity": item.quantity, "total_price": item.total_price} for item in items],
        }
        return Response(cart_data, status=status.HTTP_200_OK)

    def post(self, request):
        cart = get_or_create_cart(request)
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        product = Product.objects.get(pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response({"message": "Product added to cart."}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        cart = get_or_create_cart(request)
        product_id = request.data.get("product_id")

        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if cart_item:
            cart_item.delete()
            return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
        return Response({"error": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)
