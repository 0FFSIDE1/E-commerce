from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from customers.models import Customer
from products.models import Product
from wishlist.models import Wishlist, WishlistItem

# Create your views here.
@login_required
@require_http_methods(["POST"])
def AddToWishlist(request, pk):
    try:
        
        wishlist = Wishlist.objects.get_or_create(user=request.user)
        product = Product.objects.get(item_id=pk)
        wishlistItem = WishlistItem.objects.get_or_create(product=product, wishlist=wishlist)

        context = {
            'success': True,
            'message': 'Product added to woishlist successfully',
            'status': 'success',
        }
        return JsonResponse(context, safe=True)
    
    except Exception as e:
        context = {
            'success': False,
            'message': 'Error adding product to wishlist',
            'status': 'Error',
        }
        return JsonResponse(context, safe=True)



@login_required
@require_http_methods(["GET"])
def GetWishlist(request):
    try:
        wishlist =  Wishlist.objects.get(user=request.user)
        wishlistitem = WishlistItem.objects.get(wishlist=wishlist)
        context = {
            'success': True,
            'message': 'WishList retrieved successfully',
            'status': 'success',
            'wishlistitem': wishlistitem,

        }
        return JsonResponse(context, safe=False)

    
    except Exception as e:
        context = {
            'success': False,
            'message': 'Failed to retrive wishlist',
            'status': 'error',
        
        }
        return JsonResponse(context, safe=True)



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
    

