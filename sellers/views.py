from django.http import JsonResponse
from rest_framework import generics
from customers.models import Customer
from orders.models import Order, OrderItem
from sellers.models import Vendor
from services.serializers.vendor import LoginVendorSerializer, SellerSerializer, UpdateVendorSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, PermissionDenied
from django.contrib.auth.models import User
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from services.serializers.vendor import SellerSerializer
from sellers.models import User, Vendor
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import logging
from django.db import transaction
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from services.utils.user import staff_required, vendor_required
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.db.models.functions import TruncMonth
logger = logging.getLogger(__name__)
# Create your views here.


class RegisterVendorView(APIView):
    def get(self, request):
        return render(request, 'app/register.html')
    def post(self, request):
        """Create Vendor"""
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Use a transaction to ensure atomicity
                with transaction.atomic():
                    # Creates an AbstractBaseUser
                    user = User.objects.create_user(
                        username=serializer.validated_data['username'], 
                        email=serializer.validated_data['email'], 
                        password=serializer.validated_data['password'])
                    user.save()
                    password = serializer.validated_data.pop('password')
                    # Creates a Vendor profile (Vendor Model)
                    vendor = Vendor.objects.create(**serializer.validated_data)
                    vendor.user = user
                    vendor.save()
                    # Generate AccessToken for Vendor 
                    token = RefreshToken.for_user(user)
                    logger.debug(f"Vendor Created Successfully: {str(token.access_token)}")
                    vendor_data= SellerSerializer(vendor).data
                    context = {
                        'success': True,
                        'status': 'success', 
                        'message': 'Registration Successful', 
                        'data': {
                            'accessToken': str(token.access_token), 
                            'vendor': vendor_data,
                            }
                        }
                    return Response(context, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                logger.error(f"Error during vendor creation: {str(e)}")
                
                return Response({'success': False, 'status': 'Bad request', 'message': f'Registration unsuccessful {e}', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Handle validation errors, flattening nested errors
            def flatten_errors(errors):
                if isinstance(errors, list):
                    return ", ".join(
                        str(error) if isinstance(error, str) else str(error.get('message', error))
                        for error in errors
                    )
                return str(errors)
            error_messages = {field: flatten_errors(errors) for field, errors in serializer.errors.items()}         
            context = {
            'success': False,
            'status': 'error',
            'message': 'Some fields are invalid.',
            'errors': error_messages,
            }
            print(context)
            return Response(context, status=status.HTTP_422_UNPROCESSABLE_ENTITY,)

        
@api_view(['POST', 'GET'])
def LoginVendor(request):
    logger.info("LoginVendor view accessed")
    
    if request.method == 'POST':
        logger.info("Processing POST request for LoginVendor")
        
        serializer = LoginVendorSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            logger.debug("Received login data: username=%s", username)
            try:
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    logger.info("Authentication successful for user: %s", username)
                    token = RefreshToken.for_user(user)
                    login(request, user)
                    logger.debug("Login successful, generating token for user: %s", username)
                    context = {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            'accessToken': str(token.access_token),
                            'user': SellerSerializer(request.user.vendor).data
                        }
                    }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    logger.warning("Authentication failed for username: %s", username)
                    context = {
                        "status": "error",
                        "message": "Invalid username or password",
                        'statusCode': 401
                    }
                    return Response(context, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                logger.error("Error during login process for username: %s - %s", username, str(e), exc_info=True)
                context = {
                    "status": "error",
                    "message": f"Authentication failed due to an error: {e}",
                    'statusCode': 500
                }
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            logger.warning("Invalid data provided for login: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        logger.info("GET request received for LoginVendor, rendering login page")
        return render(request, 'app/login.html')



@login_required  
@api_view(['PATCH'])
@user_passes_test(vendor_required,  login_url='login', redirect_field_name='login')
def UpdateVendor(request):
    """Update Vendor"""
    user = request.user
    logger.info("UpdateVendor view accessed by user: %s", user)
    
    try:
        vendor = Vendor.objects.get(user=user)
        logger.info("Vendor retrieved successfully for user: %s", user)
    except Vendor.DoesNotExist:
        logger.warning("Vendor not found for user: %s", user)
        return Response({'success': False, 'message': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UpdateVendorSerializer(vendor, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                serializer.save()
                logger.info("Vendor updated successfully for user: %s", user)
                
                context = {
                    'success': True,
                    'status': 'success',
                    'message': 'Vendor updated successfully.',
                    'data': serializer.data,
                }
                return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error during vendor update for user %s: %s", user, str(e), exc_info=True)
            return Response({'success': False, 'message': f'Update failed: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        error_messages = {field: ", ".join(errors) for field, errors in serializer.errors.items()}
        logger.warning("Invalid data provided for vendor update by user %s: %s", user, error_messages)
        return Response({
            'success': False,
            'message': 'Invalid data.',
            'errors': error_messages,
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



@login_required
@require_http_methods(["GET"])
@user_passes_test(vendor_required,  login_url='login', redirect_field_name='login')
def VendorCustomersView(request):
    try:
        logger.info("VendorCustomersView called by user: %s", request.user)
        vendor = request.user.vendor  # Logged-in vendor
        logger.debug("Fetching products for vendor: %s", vendor)
        vendor_product = vendor.products.all()
        logger.debug("Products fetched: %s", vendor_product)
        order_items = OrderItem.objects.filter(product__in=vendor_product).select_related('order')
        logger.debug("Order items fetched: %s", order_items)
        customer_ids = order_items.values_list('order__customer_id', flat=True).distinct()
        customers = Customer.objects.filter(customer_id__in=customer_ids)
        logger.debug("Customers fetched: %s", customers)
        # Serialize the customer data
        customer_data = [
            {
                "id": customer.customer_id,
                "name": f"{customer.first_name} {customer.last_name}",
                "email": customer.email,
                "phone": str(customer.phone),
                "address": f"{customer.address}, {customer.city}, {customer.country}",
            }
            for customer in customers
        ]
        logger.info("Customer data successfully serialized")
        return JsonResponse({"customers": customer_data, 'total_customers': len(customer_data)}, safe=False)
    except Exception as e:
        logger.error("Error fetching customers: %s", str(e), exc_info=True)
        return JsonResponse({"success": False, "message": f"Error fetching customers: {e}"}, safe=False)



@login_required
@require_http_methods(["GET"])
@user_passes_test(vendor_required,  login_url='login', redirect_field_name='login')
def GetMonthlyOrderForVendor(request):
    try:
        vendor = request.user.vendor
        order = Order.objects.filter(cart__items__product__vendor=vendor)
        # Annotate and group orders by month
        monthly_orders = (
            order.annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(order_count=Count('order_id'))
                .order_by('month')
            )
        # Format the data for response
        result = [
                {
                    "month": item["month"].strftime("%Y-%m"),  # Format month as YYYY-MM
                    "total_order": item["order_count"],
                }
                for item in monthly_orders
            ]
        return JsonResponse({
                "success": True,
                "message": "Vendor orders retrieved successfully",
                "data": result,
            }, status=200)

    except Exception as e:
            return JsonResponse({
                "success": False,
                "message": "An error occurred while retrieving vendor orders",
                "error": str(e),
            }, status=500)
        

@login_required
@require_http_methods(["GET"])
@user_passes_test(staff_required,  login_url='login', redirect_field_name='login')
def AllVendorsView(request):
    try: 
        vendor = Vendor.objects.all()
        serialiazer = SellerSerializer(vendor, many=True)
        context = {
            'success': True,
            'message': 'Vendor retrieved successfully',
            'vendors': serialiazer.data,
            'total_vendors': len(serialiazer.data),
        }
        return JsonResponse(context, safe=True, status=200)
    except Exception as e:
        context = {
            'success': False,
            'message': f'error retrieving vendor list {e}',
        }
        return JsonResponse(context, safe=True, status=400)

    
    
