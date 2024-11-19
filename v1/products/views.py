from django.shortcuts import render
from rest_framework import generics 
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from services.serializers.product import ProductSerializer
from services.utils.product import *
from services.utils.error import Error_Response
from django.http import Http404

# Create your views here.
class Products_view(generics.ListCreateAPIView):
        """
        GET: Retrieves all Product record
        POST: Add new Product record
        queryset: All rows in Product Entity (total number of Products)
        serializer_class: All columns in Product Entity
        """
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        
        # GET
        def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()

            print(queryset)
            
            # Filter by query parameters
            category = request.query_params.get('category')  # e.g., ?category=electronics
            name = request.query_params.get('name')  # e.g., ?name=iphone
            vendor = request.query_params.get('vendor') # e.g., ?vendor=vendor
            section = request.query_params.get('section') # e.g., ?section=New arrivals
            brand = request.query_params.get('brand')  # e.g., ?brand=nike
            product_type = request.query_params.get('brand')  # e.g., ?brand=nike

            if category:
                queryset = queryset.filter(category=category.capitalize())  # Case-insensitive filter
            elif name:
                queryset = queryset.filter(name=name.capitalize())  
            elif vendor:
               queryset = queryset.filter(vendor=vendor.capitalize()) 
            elif brand:
               queryset = queryset.filter(brand=brand.capitalize())
            elif product_type:
               queryset = queryset.filter(type__icontains=product_type.capitalize())
            elif section:
                queryset = queryset.filter(section__icontains=section.capitalize())
            
            
            serializer = self.get_serializer(queryset, many=True)
            print(serializer.data)
            return Response(get_products_response(
                queryset = queryset.count(), 
                product = serializer.data),
                status = status.HTTP_200_OK,
            )

        # POST
        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(post_products_response(
                product = serializer.data,     
            ), status = status.HTTP_201_CREATED)
        

class Product_detail(generics.RetrieveUpdateDestroyAPIView):
    """
       GET: Retrieves specific Product record
       PUT and PATCH: update specific Product record
       DELETE: delete specific Product record
       queryset: all row in Product Entity
       serializer_class: All columns in Product Entity
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail=Error_Response(error="ProductNotFound", message="Product"), code=404)
       
    # def check_permissions(self, request):
    #     if not request.user.has_perm('Products.change_Product'):
    #         raise PermissionDenied({"error": "You do not have permission to update this object."})
    #     return super().check_permissions(request)

    # GET
    def retrieve(self, request, *args, **kwargs):
        Product = self.get_object()
        serializer = self.get_serializer(Product)
        return Response(retrieve_product_response_data(
            product = serializer.data,
        ), status=status.HTTP_200_OK)

    # Update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(update_product_response_data(
            product = serializer.data,
        ), status=status.HTTP_200_OK)
    
    # Delete
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(destroy_product_response_data(), 
                        status=status.HTTP_204_NO_CONTENT)