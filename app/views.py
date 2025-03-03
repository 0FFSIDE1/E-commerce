from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from app.models import Subscription, SubscriptionPlan
from services.serializers.subcription import RenewSubscriptionSerializer, SubscriptionPlanSerializer, SubscriptionSerializer
from services.utils.user import staff_required, vendor_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@login_required
@user_passes_test(vendor_required, login_url='login', redirect_field_name='login')
def index(request):
    return render(request, 'app/index.html')


class SubcriptionPlanView(APIView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(vendor_required, login_url='login', redirect_field_name='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        context = {
            'success': True,
            'message': 'Plan retrieved successfully',
            'plans': serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)
    

    def post(self, request):
        serializer = SubscriptionPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SubcriptionView(APIView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(vendor_required, login_url='login', redirect_field_name='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        subcriptions = Subscription.objects.filter(user=request.user.vendor)
        serializer = SubscriptionSerializer(subcriptions, many=True)
        context = {
            'success': True,
            'message': 'Subscripton retrieved successfully',
            'subs': serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)
    

class AddSubscriptionView(APIView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(staff_required, login_url='login', redirect_field_name='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RenewOrDeleteSubcriptionView(APIView):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(vendor_required, login_url='login', redirect_field_name='login'))
    def patch(self, request, pk):
        """
        Partially update a subscription by its ID.
        """
        try:
            subscription = Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RenewSubscriptionSerializer(subscription, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a subscription by its ID.
        """
        try:
            subscription = Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)
        
        subscription.delete()
        return Response({"message": "Subscription deleted successfully"}, status=status.HTTP_204_NO_CONTENT)






