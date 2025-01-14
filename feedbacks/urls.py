from django.urls import path
from .views import *



urlpatterns = [
   path('feedback', Feedbacks_view.as_view(), name='all-feedbacks'),
   path('<str:pk>/feedback', Feedback_detail.as_view(), name='feedback-detail'),
    
]
