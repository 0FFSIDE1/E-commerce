from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/newsletter/create', CreateNewsletter, name='create-newsletter'),
]
