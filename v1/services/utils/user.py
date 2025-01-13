
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from carts.models import Cart
from app.models import AdminUser
from django.shortcuts import get_object_or_404
# Custom decorator to check if the user is staf
def staff_required(user):
    user = get_object_or_404(AdminUser, user=user)
    if user:
        return True


@sync_to_async
def create_user(username, email, password):
    user = User.objects.create_user(username, email, password)
    return user

@sync_to_async
def check_user_exists(email):
    return User.objects.filter(email=email).exists()


def add_user_to_cart(request, user):
    cart =  Cart.objects.filter(session=request.session.session_key).update(user=user)
    
    
    return cart
            

@sync_to_async
def authenticate_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)

    return user


@sync_to_async
def check_password(password, password2):
    if password == password2:
        return True
    else:
        return False
    

@sync_to_async
def create_superuser(username, email, password):
    user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password)
    admin = AdminUser.objects.create(
        username=username,
        email=email,
        user=user,
    )
    
    return admin