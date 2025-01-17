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
    """Add a product to the user's wishlist."""
    try:
        # Log the access to the view
        logger.info("AddToWishlist view accessed by user: %s for product ID: %d", request.user, pk)

        # Get or create the wishlist for the logged-in user
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        logger.info("Wishlist retrieved or created for user: %s. Created: %s", request.user, created)

        # Get the product by its ID
        product = Product.objects.get(item_id=pk)
        logger.info("Product retrieved: %s (ID: %d)", product.name, pk)

        # Add the product to the wishlist
        wishlist_item, created = WishlistItem.objects.get_or_create(
            product=product,
            wishlist=wishlist
        )
        logger.info("Wishlist item %s for product: %s (ID: %d). Created: %s", 
                    wishlist_item, product.name, pk, created)

        return JsonResponse({
            'success': True,
            'message': 'Product added to wishlist successfully',
            'status': 'success',
        }, status=201)

    except Product.DoesNotExist:
        logger.warning("Product with ID %d not found", pk)
        return JsonResponse({
            'success': False,
            'message': 'Product not found',
            'status': 'error',
        }, status=404)

    except Exception as e:
        logger.error("Error while adding product ID %d to wishlist for user %s: %s",
                     pk, request.user, str(e), exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while adding product to wishlist',
            'status': 'error',
            'error': str(e),
        }, status=500)


@login_required
@require_http_methods(["GET"])
def GetWishlist(request):
    """Retrieve the user's wishlist."""
    try:
        # Log access to the view
        logger.info("GetWishlist view accessed by user: %s", request.user)

        # Get the user's wishlist
        wishlist = Wishlist.objects.get(user=request.user)
        logger.info("Wishlist retrieved for user: %s", request.user)

        # Retrieve all items in the wishlist
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        logger.info("Wishlist items count for user %s: %d", request.user, wishlist_items.count())

        # Check if the wishlist is empty
        if not wishlist_items.exists():
            logger.info("Wishlist is empty for user: %s", request.user)
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
        logger.info("Wishlist serialized successfully for user: %s", request.user)

        return JsonResponse({
            'success': True,
            'message': 'Wishlist retrieved successfully',
            'status': 'success',
            'wishlist_items': items,
        }, status=200)

    except Wishlist.DoesNotExist:
        logger.warning("Wishlist does not exist for user: %s", request.user)
        return JsonResponse({
            'success': False,
            'message': 'Wishlist does not exist for the user',
            'status': 'error',
        }, status=404)

    except Exception as e:
        logger.error("Error retrieving wishlist for user %s: %s", request.user, str(e), exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'Failed to retrieve wishlist',
            'status': 'error',
            'error': str(e),
        }, status=500)

@login_required
@require_http_methods(["DELETE"])
def DeleteWishlistItem(request, pk):
    """Delete an item from the wishlist."""
    try:
        logger.info("DeleteWishlistItem view accessed by user: %s", request.user)

        # Retrieve the wishlist item by its ID
        wishlistitem = WishlistItem.objects.get(pk=pk)
        logger.info("Wishlist item found: ID %s for user %s", pk, request.user)

        # Delete the item
        wishlistitem.delete()
        logger.info("Wishlist item ID %s successfully deleted for user %s", pk, request.user)

        context = {
            'success': True,
            'message': 'Item removed from wishlist',
            'status': 'Success',
        }
        return JsonResponse(context, safe=True)

    except WishlistItem.DoesNotExist:
        logger.warning("Wishlist item with ID %s not found for user %s", pk, request.user)
        context = {
            'success': False,
            'message': 'Wishlist item not found',
            'status': 'Error',
        }
        return JsonResponse(context, safe=True, status=404)

    except Exception as e:
        logger.error("Error deleting wishlist item ID %s for user %s: %s", pk, request.user, str(e), exc_info=True)
        context = {
            'success': False,
            'message': 'Error deleting wishlist item',
            'status': 'Error',
        }
        return JsonResponse(context, safe=True, status=500)

