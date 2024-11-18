from django.shortcuts import render
from rest_framework import generics 
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Feedback
from rest_framework import status
from services.serializers.feedback import FeedbackSerializer
from services.utils.feedback import *
from services.utils.error import Error_Response
from django.http import Http404

# Create your views here.
class Feedbacks_view(generics.ListCreateAPIView):
        """
        GET: Retrieves all Feedback record
        POST: Add new Feedback record
        queryset: All rows in Feedback Entity (total number of Feedbacks)
        serializer_class: All columns in Feedback Entity
        """
        queryset = Feedback.objects.all()
        serializer_class = FeedbackSerializer
        
        # GET
        def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(get_feedbacks_response(
                queryset = queryset.count(), 
                feedback = serializer.data),
                status = status.HTTP_200_OK,
            )

        # POST
        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(post_feedbacks_response(
                feedback = serializer.data,     
            ), status = status.HTTP_201_CREATED)
        

class Feedback_detail(generics.RetrieveUpdateDestroyAPIView):
    """
       GET: Retrieves specific Feedback record
       PUT and PATCH: update specific Feedback record
       DELETE: delete specific Feedback record
       queryset: all row in Feedback Entity
       serializer_class: All columns in Feedback Entity
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail=Error_Response(error="FeedbackNotFound", message="Feedback"), code=404)
       
    # def check_permissions(self, request):
    #     if not request.user.has_perm('Feedbacks.change_Feedback'):
    #         raise PermissionDenied({"error": "You do not have permission to update this object."})
    #     return super().check_permissions(request)

    # GET
    def retrieve(self, request, *args, **kwargs):
        Feedback = self.get_object()
        serializer = self.get_serializer(Feedback)
        return Response(retrieve_feedback_response_data(
            feedback = serializer.data,
        ), status=status.HTTP_200_OK)

    # Update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(update_feedback_response_data(
            feedback = serializer.data,
        ), status=status.HTTP_200_OK)
    
    # Delete
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(destroy_feedback_response_data(), 
                        status=status.HTTP_204_NO_CONTENT)