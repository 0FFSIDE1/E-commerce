from django.shortcuts import render
from rest_framework import generics 
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Notification
from rest_framework import status
from services.serializers.notification import NotificationSerializer
from services.utils.error import Error_Response
from django.http import Http404
from services.utils.notification import *

# Create your views here.
class Notifications_view(generics.CreateAPIView):
        """
        GET: Retrieves all notification record
        POST: Add new notification record
        queryset: All rows in notification Entity (total number of notifications)
        serializer_class: All columns in notification Entity
        """
        queryset = Notification.objects.all()
        serializer_class = NotificationSerializer
    
        # POST
        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(post_notifications_response(
                notification = serializer.data,     
            ), status = status.HTTP_201_CREATED)
        

class Notification_detail(generics.RetrieveUpdateDestroyAPIView):
    """
       GET: Retrieves specific notification record
       PUT and PATCH: update specific notification record
       DELETE: delete specific notification record
       queryset: all row in notification Entity
       serializer_class: All columns in notification Entity
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail=Error_Response(error="NotificationNotFound", message="Notification"), code=404)
       
    # def check_permissions(self, request):
    #     if not request.user.has_perm('notifications.change_notification'):
    #         raise PermissionDenied({"error": "You do not have permission to update this object."})
    #     return super().check_permissions(request)

    # GET
    def retrieve(self, request, *args, **kwargs):
        notification = self.get_object()
        serializer = self.get_serializer(notification)
        return Response(retrieve_notification_response_data(
            notification = serializer.data,
        ), status=status.HTTP_200_OK)

    
    # Delete
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(destroy_notification_response_data(), 
                        status=status.HTTP_204_NO_CONTENT)