import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Newsletter
from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(["POST"])
def CreateNewsletter(request):

    try:
        data = json.loads(request.body)
        newsletter= Newsletter.objects.create(email=data.get('email'))
        context = {
            'success': True,
            'message': 'Thank you for subscribing to our newsletter!',
            'status': 'success',
        }
        return JsonResponse(context, safe=True)

    except Exception as e:
        context = {
                'success': False,
                'message': 'Error subscribing to newsletter try again later!',
                'status': 'error',
            }
        return JsonResponse(context, safe=True)
