import json
from django.shortcuts import render
from rest_framework import generics 
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from customers.models import Customer
from orders.models import Order
from sellers.models import Vendor
from services.serializers.review import OrderReviewSerializer, ProductReviewSerializer, VendorReviewSerializer
from .models import OrderReview, ProductReview, VendorReview
from rest_framework import status
# from services.serializers.review import ProductReviewSerializer, ReviewSerializer
# from services.utils.response.error import Error_Response
from django.http import JsonResponse
from products.models import Product
from services.utils.response.review import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

# # Create your views here.
@login_required
@require_http_methods(["POST"])
def CreateProductReview(request, pk):
    try: 
        data = json.loads(request.body)
        customer = Customer.objects.get(user=request.user)
        product = Product.objects.get(item_id=pk)
        review = ProductReview.objects.get_or_create(customer=customer, product=product, message=data.get('message'), rating=data.get('rating'))
      
        context = {
            'success': True,
            'message': 'Thanks for your review',
            'status': 'success',
        
        }
        return JsonResponse(context, safe=True, status=201)
    except Exception as e:
        context = {
            'success': False,
            'message': 'Error adding review try again later',
            'status': 'error',
        
        }
        return JsonResponse(context, safe=True, status=404)


@require_http_methods(["GET"]) 
def ProductReviewDetail(request, pk):
    try:
        review = ProductReview.objects.get(pk=pk)
        serializer = ProductReviewSerializer(review)
        context = {
            'success': True,
            'message': 'Retrieved successfully',
            'review': serializer.data,
        }
        return JsonResponse(context, safe=True)
    except Exception as e:
        context = {
            'success': False,
            'message': f'Error retriving review {e}',
        }
        return JsonResponse(context, safe=True)

@login_required
@require_http_methods(["POST"])
def CreateOrderReview(request, pk):
    try: 
        data = json.loads(request.body)
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.get(order_id=pk)

        review = OrderReview.objects.get_or_create(customer=customer, order=order, message=data.get('message'), rating=data.get('rating'))

        context = {
            'success': True,
            'message': 'Thanks for your review',
            'status': 'success',
        
        }
        return JsonResponse(context, safe=True)
    except Exception as e:
        context = {
            'success': False,
            'message': f'Error adding review try again later{e}',
            'status': 'error',
        
        }
        return JsonResponse(context, safe=True)

@require_http_methods(["GET"])  
def OrderReviewDetail(request, pk):
    try:
        review = OrderReview.objects.get(pk=pk)
        serializer = OrderReviewSerializer(review)
        context = {
            'success': True,
            'message': 'Retrieved successfully',
            'review': serializer.data,
        }
        return JsonResponse(context, safe=True)
    except Exception as e:
        context = {
            'success': False,
            'message': f'Error retriving review {e}',
        }
        return JsonResponse(context, safe=True)

@login_required
@require_http_methods(["POST"])
def CreateVendorReview(request, pk):
    try: 
        data = json.loads(request.body)
        customer = Customer.objects.get(user=request.user)
        vendor = Vendor.objects.get(vendor_id=pk)

        review = VendorReview.objects.get_or_create(customer=customer, vendor=vendor, message=data.get('message'), rating=data.get('rating'))

        context = {
            'success': True,
            'message': 'Thanks for your review',
            'status': 'success',
        
        }
        return JsonResponse(context, safe=True)
    except Exception as e:
        context = {
            'success': False,
            'message': 'Error adding review try again later',
            'status': 'error',
        
        }
        return JsonResponse(context, safe=True)
    

@require_http_methods(["GET"])
def VendorReviewDetail(request, pk):
    try:
        review = VendorReview.objects.get(pk=pk)
        serializer = VendorReviewSerializer(review)
        context = {
            'success': True,
            'message': 'Retrieved successfully',
            'review': serializer.data,
        }
        return JsonResponse(context, safe=True)
    except Exception as e:
        context = {
            'success': False,
            'message': f'Error retriving review {e}',
        }
        return JsonResponse(context, safe=True)