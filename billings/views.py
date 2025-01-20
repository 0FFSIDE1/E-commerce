import json
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Payment
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class InitiatePaymentView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            amount = data.get('amount')

            pk = settings.PAYSTACK_PUBLIC_KEY
            payment = Payment.objects.create(amount=amount, email=email, user=request.user)
            payment.save()

            context = {
                'success': True,
                'payment': payment,
                'paystack_pub_key': pk,
                'amount_value': payment.amount_value(),
            }
            return Response(context,  status=status.HTTP_201_CREATED)
        except Exception as e:
            context = {
                'success': False,
                'message': f'Erorr occcured trying to initate payment {e}'
            }
            return Response(context,  status=status.HTTP_400_BAD_REQUEST)
        
class VerifyPaymentView(APIView):
    def get(self, request, ref):

        try:
            payment = Payment.objects.get(ref=ref)
            verified = payment.verify_payment()
            if verified:
                print('Payment was successful! wallet funded')
                context = {
                    'success': True,
                    'message': 'Payment Successful, Funds are in your account',
                }
                return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {
                    'success': False,
                    'message': f"Could'nt Verify payment with id {ref}",
                }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

            

