import json
import logging
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from .models import Payment
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
# Create your views here.

logger = logging.getLogger(__name__)

class InitiatePaymentView(APIView):
    def post(self, request):
        try:
            # Parse and validate request body
            data = json.loads(request.body)
            email = data.get('email')
            amount = data.get('amount')
            
            if not email or not amount:
                return Response(
                    {"success": False, "message": "Email and amount are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not isinstance(amount, (int, float)) or amount <= 0:
                return Response(
                    {"success": False, "message": "Amount must be a positive number."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Retrieve Paystack public key
            pk = getattr(settings, "PAYSTACK_PUBLIC_KEY", None)
            if not pk:
                return Response(
                    {"success": False, "message": "Payment system configuration is missing."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Create payment record within a transaction
            with transaction.atomic():
                payment = Payment.objects.create(amount=amount, email=email, user=request.user)

            # Prepare response context
            context = {
                "success": True,
                "payment_id": payment.payment_id,  # Use ID instead of exposing full object
                "paystack_public_key": pk,
                "amount_value": payment.amount_value(),
                'message': 'Payment Initiated successfully'
            }
            print(context)
            return Response(context, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body.", exc_info=True)
            return Response(
                {"success": False, "message": "Invalid JSON payload."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error initiating payment: {e}", exc_info=True)
            return Response(
                {"success": False, "message": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class VerifyPaymentView(APIView):
    def get(self, request, ref):
        try:
            # Retrieve the payment record or return 404
            payment = Payment.objects.get(ref=ref)

            # Verify the payment
            verified = payment.verify_payment()

            if verified:
                logger.info(f"Payment {ref} verified successfully.")
                return Response(
                    {
                        "success": True,
                        "message": "Payment Successful, funds are now in your account.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                logger.warning(f"Payment {ref} verification failed.")
                return Response(
                    {
                        "success": False,
                        "message": "Payment verification failed. Please contact support.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Payment.DoesNotExist:
            logger.error(f"Payment with ref {ref} does not exist.")
            return Response(
                {
                    "success": False,
                    "message": f"Payment with reference {ref} not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error verifying payment with ref {ref}: {e}", exc_info=True)
            return Response(
                {
                    "success": False,
                    "message": f"An error occurred while verifying payment: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            

