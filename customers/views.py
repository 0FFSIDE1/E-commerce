import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from customers.models import Customer
from django.contrib import messages
from services.utils.customer import create_customer, check_customer_exists, get_customer, get_customer_details, update_customer
from services.utils.user import check_user_exists, create_user, staff_required
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

@login_required
@user_passes_test(staff_required,  login_url='login', redirect_field_name='login')
@csrf_exempt
def DeleteCustomerView(request, pk):
    if request.method == 'POST':
        try:
            customer = Customer.objects.get(customer_id=pk)
            customer.delete()
            messages.success(request, 'Customer deleted successfully!')
            return JsonResponse({'success': True}, safe=True)
        except Exception as e:
            messages.error(request, f'Customer deletion Failed! {str(e)}')
            return JsonResponse({'success': False}, safe=True)


   

async def CreateCustomerView(request):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, safe=True, status=405)

    try:
        data = json.loads(request.body)
       
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        city = data.get('city')
        country = data.get('country')
        create_account = data.get('create_account')

        if create_account:
            if await check_user_exists(email):
                customer = await update_customer(request.session.session_key, first_name, last_name, address, phone, email, city, country)
                return JsonResponse({'success': True, 'message': 'Customer updated successfully!'}, safe=True, status=200)
            if await check_customer_exists(email):
                customer = await update_customer(request.session.session_key, first_name, last_name, address, phone, email, city, country, )
                return JsonResponse({'success': True, 'message': 'Customer updated successfully!'}, safe=True, status=200)
            user = await create_user(email, email, last_name)
            customer = await create_customer(user, first_name, last_name, address, phone, email, city, country)
            # await authenticate_user(request=request, username=email, password=last_name)
            
            return JsonResponse({'success': True, 'message': 'Customer created successfully!'}, safe=True, status=200)

        if await check_customer_exists(email):
            customer = await update_customer(request.session.session_key, first_name, last_name, address, phone, email, city, country)
            return JsonResponse({'success': True, 'message': 'Customer updated successfully!'}, safe=True, status=200)
        else:
            customer = await create_customer(None, first_name, last_name, address, phone, email, city, country)
            return JsonResponse({'success': True, 'message': 'Customer created successfully!'}, safe=True, status=200)

    except IntegrityError as e:
        
        return JsonResponse({'success': False, 'message': f'{e}'}, safe=True, status=400)
    except Exception as e:
        
        return JsonResponse({'success': False, 'message': str(e)}, safe=True, status=500)
    

def GetCustomer(request):
    try:
        customer = Customer.objects.get(session=request.session.session_key)
    except Customer.DoesNotExist:
        if request.user.is_authenticated:
            try:
                customer = Customer.objects.get(user=request.user)
            except Customer.DoesNotExist:
                customer = None
        else:
            customer = None
    except Exception as e:
        customer = None

    if customer:
        customer_data = {
            'id': customer.customer_id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'address': customer.address,
            'city': customer.city,
            'country': customer.country,
            'email': customer.email,
            'phone': str(customer.phone),  
            
        }
        data = {
            'success': True,
            'message': 'Customer details retrieved successfully',
            'customer': customer_data
        }
    else:
        data = {
            'success': False,
            'message': 'Customer not found'
        }

    return JsonResponse(data)
