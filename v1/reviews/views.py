from django.shortcuts import render
from rest_framework import generics 
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Review
from rest_framework import status
from services.serializers.review import ReviewSerializer
from services.utils.response.error import Error_Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from products.models import Product
from services.utils.response.review import *

# Create your views here.
class Reviews_view(generics.ListCreateAPIView):
        """
        GET: Retrieves all review record
        POST: Add new review record
        queryset: All rows in review Entity (total number of reviews)
        serializer_class: All columns in review Entity
        """
        queryset = Review.objects.all()
        serializer_class = ReviewSerializer

        # GET
        def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(get_reviews_response(
                queryset = queryset.count(), 
                review = serializer.data),
                status = status.HTTP_200_OK,)
    
        # POST
        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(post_reviews_response(
                review = serializer.data,     
            ), status = status.HTTP_201_CREATED)
        

class Review_detail(generics.RetrieveUpdateDestroyAPIView):
    """
       GET: Retrieves specific review record
       PUT and PATCH: update specific review record
       DELETE: delete specific review record
       queryset: all row in review Entity
       serializer_class: All columns in review Entity
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail=Error_Response(error="reviewNotFound", message="review"), code=404)
       
    # def check_permissions(self, request):
    #     if not request.user.has_perm('reviews.change_review'):
    #         raise PermissionDenied({"error": "You do not have permission to update this object."})
    #     return super().check_permissions(request)

    # GET
    def retrieve(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(review)
        return Response(retrieve_review_response_data(
            review = serializer.data,
        ), status=status.HTTP_200_OK)

    
    # Delete
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(destroy_review_response_data(), 
                        status=status.HTTP_204_NO_CONTENT)
    


    
    
    