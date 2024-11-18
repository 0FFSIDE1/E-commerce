from django.urls import path
from .views import *



urlpatterns = [
   path('', Feedbacks_view.as_view(), name='all-feedbacks'),
   path('', Feedback_detail.as_view(), name='feedback-detail'),
    
]
