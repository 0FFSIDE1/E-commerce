from django.urls import path
from .views import *



urlpatterns = [
   path('auth/dashboard/vendor/register', RegisterVendorView.as_view(), name='create_vendor'),
   path("profile/<str:name>", Profile_View.as_view()),
   path("adminview/<str:name>", All_View.as_view()),
   path("update/<str:name>", Update_View.as_view()),
   # path("retrieve/<str:name>", retrieve.as_view())
]
