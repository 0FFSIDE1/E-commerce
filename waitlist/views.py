from django.shortcuts import render
from rest_framework import generics
from waitlist.models import Waitlist
from services.serializers.waitlist import WaitlistVendorSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class WaitlistVendors(generics.CreateAPIView):
    queryset = Waitlist.objects.all()
    serializer_class = WaitlistVendorSerializer
    @swagger_auto_schema(
        operation_description="Add a vendor to the waitlist",
        request_body=WaitlistVendorSerializer,
        responses={
            201: WaitlistVendorSerializer(),
            400: "Bad Request - Invalid input data",
            422: "Unprocessable Entity",
            500: "Internal Server Error",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    