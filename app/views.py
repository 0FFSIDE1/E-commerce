from django.shortcuts import render
from services.serializers.vendor import LoginVendorSerializer, SellerSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


def index(request):
    return render(request, 'app/index.html')