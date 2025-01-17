from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from customers.models import Customer
from products.models import Product
from wishlist.models import Wishlist, WishlistItem
import logging

logger = logging.getLogger(__name__)

# Create your views here.
@login_required
@require_http_methods(["POST"])
def AddToWishlist(request, pk):
    try:
        # Get or create the wishlist for the logged-in user
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        print(f"Wishlist: {wishlist}")
        # Get the product by its ID
        product = Product.objects.get(item_id=pk)
        print(f"product: {product}")

        # Add the product to the wishlist
        wishlist_item, created = WishlistItem.objects.get_or_create(
            product=product,
            wishlist=wishlist
        )
        print(f"wishlist_item: {wishlist_item}")

        return JsonResponse({
            'success': True,
            'message': 'Product added to wishlist successfully',
            'status': 'success',
        }, status=201)

    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found',
            'status': 'error',
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while adding product to wishlist',
            'status': 'error',
            'error': str(e),
        }, status=500)


@login_required
@require_http_methods(["GET"])
def GetWishlist(request):
    try:
        # Get the user's wishlist
        wishlist = Wishlist.objects.get(user=request.user)
        print(f"user: {wishlist}")

        # Retrieve all items in the wishlist
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

        # Check if the wishlist is empty
        if not wishlist_items.exists():
            return JsonResponse({
                'success': True,
                'message': 'Wishlist is empty',
                'status': 'success',
                'wishlist_items': [],
            }, status=200)

        # Serialize the wishlist items
        items = [
            {
                'id': item.id,
                'product_name': item.product.name,
                'product_id': item.product.item_id,
                'price': str(item.product.price),
                'added_at': item.added_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for item in wishlist_items
        ]

        return JsonResponse({
            'success': True,
            'message': 'Wishlist retrieved successfully',
            'status': 'success',
            'wishlist_items': items,
        }, status=200)

    except Wishlist.DoesNotExist:
        logger.warning(f"Wishlist does not exist for user: {request.user}")
        return JsonResponse({
            'success': False,
            'message': 'Wishlist does not exist for the user',
            'status': 'error',
        }, status=404)

    except Exception as e:
        logger.error(f"Error retrieving wishlist for user {request.user}: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Failed to retrieve wishlist',
            'status': 'error',
            'error': str(e),
        }, status=500)

@login_required
@require_http_methods(["DELETE"])
def DeleteWishlistItem(request, pk):
    try:
        wishlistitem = WishlistItem.objects.get(pk=pk)
        wishlistitem.delete()
        context = {
            'success': True,
            'message': 'Item removed from wishlist',
            'status': 'Error',
        }
        return JsonResponse(context, safe=True)
    
    except Exception as e:
        context = {
            'success': False,
            'message': 'Error deleting wishlist',
            'status': 'Error',
        }
        return JsonResponse(context, safe=True)
    

