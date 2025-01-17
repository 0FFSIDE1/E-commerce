import json
from django.shortcuts import get_object_or_404, render
from rest_framework import generics 
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, user_passes_test
from services.utils.user import staff_required, vendor_required
from .models import Feedback
from rest_framework import status
from services.serializers.feedback import FeedbackSerializer
from services.utils.response.feedback import *
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def CreateFeedback(request):
    try:
        data = json.loads(request.body)
        message = data.get('message')
        

        if not message:
            context = {
            'success': False,
            'message': 'Message field is required.',
            'status': 'error',
        }
            return JsonResponse(context, status=status.HTTP_400_BAD_REQUEST)
        
        feedback = Feedback.objects.create(email=data.get('email'), message=data.get('message'))
        
       
        context = {
            'success': True,
            'message': 'Thanks for your feedback. We appreciate your response!',
            'status': 'succcess',
        }
        return JsonResponse(context, safe=True, status=201)
    
    except Exception as e:
        context = {
            'success': False,
            'message': f'An error occured try again later! {e}',
            'status': 'error',
        }
        return JsonResponse(context, safe=True, status=400)


@login_required
@require_http_methods(["GET"]) 
@user_passes_test(staff_required, login_url='login', redirect_field_name='login')
def GetFeedback(request):
    try:
        # Retrieve all feedback records
        feedback = Feedback.objects.all()

        # Serialize the feedback list (many=True for multiple objects)
        serializer = FeedbackSerializer(feedback, many=True)

        # Return success response
        return JsonResponse({
            'success': True,
            'message': 'Feedback retrieved successfully',
            'feedback': serializer.data,
            'status': 'success',
        }, safe=False, status=200)

    except Exception as e:
        # Handle any unexpected exceptions
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving feedbacks: {str(e)}',
            'status': 'error',
        }, safe=True, status=400)
    


@login_required
@require_http_methods(["GET"]) 
@user_passes_test(staff_required, login_url='login', redirect_field_name='login')
def GetFeedbackDetail(request, pk):
    try:
        # Get the feedback by primary key
        feedback = get_object_or_404(Feedback, pk=pk)

        # Serialize the feedback
        serializer = FeedbackSerializer(feedback)

        # Response context
        return JsonResponse({
            'success': True,
            'message': 'Feedback retrieved successfully',
            'status': 'success',
            'feedback': serializer.data,
        }, safe=True, status=200)

    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving feedback: {str(e)}',
            'status': 'error',
        }, safe=True, status=400)
