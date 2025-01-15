from rest_framework import generics
from sellers.models import Vendor
from services.serializers.vendor import LoginVendorSerializer, SellerSerializer
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
                    
                    # Remove password from validated_data to prevent issues with the vendor model
                    password = serializer.validated_data.pop('password')
                    
                    # Creates a Vendor profile (Vendor Model)
                    vendor = Vendor.objects.create(**serializer.validated_data)
                    # Assign AbstractBaseUser to Vendor model, i.e the owner of the Vendor Model. OnetoOnerelationship is estabilshed between User and Vendor Model
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
    if request.method == 'POST':
        serializer = LoginVendorSerializer(data=request.data)

        if serializer.is_valid():
            username= serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    token = RefreshToken.for_user(user)
                    login(request, user)
                    context = {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            'accessToken': str(token.access_token),
                            'user': SellerSerializer(request.user.vendor).data
                        }
                    }
                    return Response(context, status=status.HTTP_200_OK)
            except Exception as e:
                context = {
                    "status": f"error {e}",
                    "message": "Authetication Failed",
                    'statusCode': 401
                }
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)
                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return render(request, 'app/login.html')
        

# To view account based on auth
class Profile_View(generics.RetrieveAPIView):
    serializer_class = SellerSerializer
    lookup_url_kwarg = "name"
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        name = self.kwargs.get(self.lookup_url_kwarg)
        if not name:
            return NotFound("Name not found")
        if user.is_staff:
            return Vendor.objects.all()

        return Vendor.objects.filter(name=name)

    def get_object(self):
        queryset = self.get_queryset()
        name = self.kwargs.get(self.lookup_url_kwarg)

        if not name:
            raise NotFound("Name not provided.")

        # Filter the queryset by name
        obj = queryset.filter(name=name).first()
        if not obj:
            raise NotFound(f"No profile found for name: {name}.")
        return obj
    
# Admin to see all vendors
class All_View(generics.ListAPIView):
    serializer_class = SellerSerializer
    queryset = Vendor.objects.all()
    lookup_url_kwarg = "name"

    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwarg)
        if not name:
            raise NotFound("Staff name not provided.")

        try:
            # Check if the name corresponds to a staff user
            User.objects.get(username=name, is_staff=True)
        except User.DoesNotExist:
            raise PermissionDenied("Only staff members can view all vendor profiles.")
        
        # If the user is staff, return all vendor profiles
        return Vendor.objects.all()
    
    
# To update
class Update_View(generics.RetrieveUpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "name"
    lookup_field = "name"

    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwarg)
        if not name:
            raise NotFound("No name parameter found in the URL.")

        queryset = Vendor.objects.filter(name=name)
        if not queryset.exists():
            raise NotFound(f"No user found with the name '{name}'.")
        return queryset
    
# class retrieve(generics.RetrieveUpdateAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = SellerSerializer
#     permission_classes = [AllowAny]
#     lookup_url_kwarg = "name"
#     lookup_field = "name"