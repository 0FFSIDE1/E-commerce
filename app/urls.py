from django.urls import path
from .views import *



urlpatterns = [
   # path('', Customers_view.as_view(), name='all-customers'),
   # path('<str:pk>/customer', Customer_detail.as_view(), name='customer-detail'),
   
   path('v1/vendor/dashboard', index, name="dashboard"),
   path('api/v1/subscription/plans', SubcriptionPlanView.as_view(), name="subscription-plans"),
   path('api/v1/subscriptions', SubcriptionView.as_view(), name="subscriptions"),
   path('api/v1/subscriptions/create', AddSubscriptionView.as_view(), name="create-subscriptions"),
   path('api/v1/subscription/<int:pk>/update', RenewOrDeleteSubcriptionView.as_view(), name="update-subscription"),

   
]
