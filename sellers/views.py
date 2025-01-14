from rest_framework import generics
from sellers.models import Vendor
from services.serializers.vendor import SellerSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from django.contrib.auth.models import User
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from services.serializers.vendor import SellerSerializer
from sellers.models import User, Vendor
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__)
# Create your views here.

class RegisterVendorView(APIView):
    def get(self, request):
        context = {
	        "full_name": "Enter First name",
	        "brand_name": "Enter Last name",
	        "email": "Enter a valid email",
            "address": "Enter an address",
	        "password": "Enter password",
	        "phone": "Enter phone number",
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Create Vendor"""
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Creates an AbstractBaseUser
                user = User.objects.create_user(
                    username=serializer.validated_data['full_name'], 
                    email=serializer.validated_data['email'], 
                    password=serializer.validated_data['password'])
                user.save()
                print(user)
                
                # Remove password from validated_data to prevent issues with the model
                password = serializer.validated_data.pop('password')
                print(password)

                # Creates a Vendor profile (Vendor Model)
                vendor = Vendor.objects.create(**serializer.validated_data)
                # Assign AbstractBaseUser to Vendor model, i.e the owner of the User Model. OnetoOnerelationship is estabilshed between User and Vendor Model
                vendor.user = user
                vendor.save()
                
                # Generate AccessToken for Vendor 
                token = RefreshToken.for_user(user)
                logger.info(f"Vendor Created Successfully: {str(token.access_token)}")
               
                return Response({'status': 'success', 'message': 'Registration successful', 'data': {'accessToken': str(token.access_token), 'vendor': SellerSerializer(vendor).data}}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                logger.error(f"Error during vendor creation: {str(e)}")
                
                return Response({'status': 'Bad request', 'message': 'Registration unsuccessful', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)
            
        context = {
            "errors": serializer.errors
        }
        return Response(context, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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