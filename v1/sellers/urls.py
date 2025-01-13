from django.urls import path
from .views import *



urlpatterns = [
   path('', Create_View.as_view(), name='create_view'),
   path("profile/<str:name>", Profile_View.as_view()),
   path("adminview/<str:name>", All_View.as_view()),
   path("update/<str:name>", Update_View.as_view()),
   # path("retrieve/<str:name>", retrieve.as_view())
]
