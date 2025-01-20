from django.urls import path
from .views import *



urlpatterns = [
   path('api/v1/initiate/payment', InitiatePaymentView.as_view(), name='initiate_payment'),
   path('api/v1/verify/<str:ref>/payment', VerifyPaymentView.as_view(), name='verify-payment'),
    
]
