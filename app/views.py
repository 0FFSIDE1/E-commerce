from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from services.utils.user import vendor_required

# Create your views here.

@login_required
@user_passes_test(vendor_required, login_url='login', redirect_field_name='login')
def index(request):
    return render(request, 'app/index.html')