from django.shortcuts import render
from services.serializers.vendor import LoginVendorSerializer, SellerSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required, user_passes_test
from services.utils.user import vendor_required

# Create your views here.

@login_required
@user_passes_test(vendor_required, login_url='login', redirect_field_name='login')
def index(request):
    return render(request, 'app/index.html')