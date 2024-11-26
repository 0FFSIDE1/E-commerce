from customers.models import Customer
from django.core.exceptions import ObjectDoesNotExist

async def get_customer(request):
    try:
        customer = Customer.objects.get(user=request.user)
    
    except ObjectDoesNotExist:
        customer = Customer.objects.get(session=request.session.session_key)

    return customer
        