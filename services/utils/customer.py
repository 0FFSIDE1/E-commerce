from customers.models import Customer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async

# Wrap synchronous ORM calls with sync_to_async

@sync_to_async
def get_customer(user, session):
    """
    Retrieve  a customer 

    Args:
        user: for authenticated users.
        session: for anonymous customers/unautheticated users.

    Returns:
        customer object for the specified customer or session.

    Raises:
        ValueError: If neither user nor session is provided.
    """
    

    try:
    
        # Retrieve or create a customer for a specific customer
        customer, created = Customer.objects.get(user=user)
       
       
    except Exception as e:
        customer = get_object_or_404(Customer, session=session)
        
    
    return customer


@sync_to_async
def create_customer(user, full_name, address, phone, email, city, country):
    """
    Create a customer

    Args:
        user: for authenticated users.
        full_name: first name of the customer.
        
        address: address of the customer.
        phone: phone number of the customer.
        email: email address of the customer.

    Returns:
        customer object for the specified customer.

    Raises:
        ValueError: If user is not provided.
    """
    if user is not None:
        customer = Customer.objects.create(user=user, full_name=full_name, address=address, phone=phone, email=email, city=city, country=country)
    
        return customer

    try:
        # Create a customer for a specific user
        customer = Customer.objects.create(full_name=full_name, address=address, phone=phone, email=email, city=city, country=country)
        
        return customer
    except Exception as e:
        raise ValueError(f"Error creating customer: {str(e)}")
    

@sync_to_async
def check_customer_exists(email):
    """
    Check if a customer exists

    Args:
        email: email address of the customer.

    Returns:
        True if customer exists, False otherwise.
    """
    try:
        customer = Customer.objects.get(email=email)
        return True
    except ObjectDoesNotExist:
        return False
    
    
@sync_to_async
def update_customer(session, full_name, address, phone, email, city, country):
    """
    Update customer details

    Args:
        full_name: First name of the customer.
        
        address: Address of the customer.
        phone: Phone number of the customer.
        email: Email address of the customer.
        city: City of the customer.
        country: Country of the customer.

    Returns:
        Updated customer object.
    """
    try:
        customer = Customer.objects.get(email=email)
        customer.session = session
        customer.full_name = full_name
        customer.address = address
        customer.phone = phone
        customer.city = city
        customer.country = country
        customer.save()
        return customer
    except Customer.DoesNotExist:
        raise ValueError("Customer does not exist")
    
@sync_to_async
def get_customer_details(customer):
    customer_data = {
                'full_name': customer.full_name,
                'email': customer.email,
                'phone': str(customer.phone),
                'address': customer.address,
                'city': customer.city,
                'country': customer.country,
            }
    return customer_data
