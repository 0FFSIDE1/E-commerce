from rest_framework import generics
from sellers.models import Vendor
from services.serializers.vendor import SellerSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from django.contrib.auth.models import User

# To create an account
class Create_View(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [AllowAny]

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